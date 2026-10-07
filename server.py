"""Bench: a local learning platform for Oussema's 12-week plan.

Start it from your project's virtual environment so your code runs with your packages:
    python server.py
Then open http://127.0.0.1:8765
"""
import base64
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import curriculum as curriculum_module
import curriculum_week1
import lab_files
from lab_files import check_path

ROOT = Path(__file__).resolve().parent
LAB_DIR = Path(os.environ.get("LAB_DIR", ROOT.parent / "ml-fundamentals-lab")).resolve()
# Your progress is personal data that changes every minute, so it lives in a file git
# ignores. progress.json (tracked) is only read once, to carry old progress over.
PROGRESS_FILE = ROOT / "progress.local.json"
LEGACY_PROGRESS_FILE = ROOT / "progress.json"
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", "60"))
PORT = int(os.environ.get("PORT", "8766"))

DAY_RE = re.compile(r"^day\d{2}$")
NAME_RE = re.compile(r"^[\w\-. ]+$")

app = FastAPI(title="Bench")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
_progress_lock = threading.Lock()


def safe_path(day: str, name: str) -> Path:
    if not DAY_RE.match(day) or not NAME_RE.match(name) or ".." in name:
        raise HTTPException(400, "Invalid day folder or file name.")
    path = (LAB_DIR / day / name).resolve()
    if LAB_DIR not in path.parents:
        raise HTTPException(400, "Path escapes the lab folder.")
    return path


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


def load_curriculum():
    """Re-read the curriculum on every page load, so a new week's plan, a branch switch
    or an edited brief shows up after a browser refresh, without restarting Bench."""
    for module in (lab_files, curriculum_week1, curriculum_module):
        importlib.reload(module)
    return curriculum_module.CURRICULUM


@app.get("/api/curriculum")
def curriculum():
    return {"weeks": load_curriculum(), "lab_dir": str(LAB_DIR)}


@app.get("/api/progress")
def get_progress():
    for path in (PROGRESS_FILE, LEGACY_PROGRESS_FILE):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


@app.post("/api/progress")
def save_progress(progress: dict):
    with _progress_lock:
        tmp = PROGRESS_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(PROGRESS_FILE)
    return {"ok": True}


@app.get("/api/file")
def read_file(day: str, name: str):
    path = safe_path(day, name)
    if not path.exists():
        return {"exists": False, "content": ""}
    return {"exists": True, "content": path.read_text(encoding="utf-8", errors="replace")}


class FileIn(BaseModel):
    day: str
    name: str
    content: str


@app.post("/api/file")
def write_file(body: FileIn):
    path = safe_path(body.day, body.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.content, encoding="utf-8")
    return {"ok": True}


class RunIn(BaseModel):
    day: str
    name: str | None = None  # None = run a lesson snippet
    code: str


# A plain `def` endpoint: FastAPI runs it in a thread pool, so a long-running
# script doesn't freeze the server. (That's the Day 2 lesson in action.)
@app.post("/api/run")
def run(body: RunIn):
    if not DAY_RE.match(body.day):
        raise HTTPException(400, "Invalid day folder.")
    day_dir = LAB_DIR / body.day
    day_dir.mkdir(parents=True, exist_ok=True)

    if body.name:
        target = safe_path(body.day, body.name)
        target.write_text(body.code, encoding="utf-8")
    else:
        scratch = LAB_DIR / ".scratch"
        scratch.mkdir(exist_ok=True)
        target = scratch / "snippet.py"
        target.write_text(body.code, encoding="utf-8")

    fig_dir = Path(tempfile.mkdtemp(prefix="bench_figs_"))
    env = {**os.environ, "MPLBACKEND": "Agg", "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"}
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "runner.py"), str(target), str(fig_dir)],
            cwd=day_dir, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=RUN_TIMEOUT, env=env,
        )
        stdout, stderr, code, timed_out = proc.stdout, proc.stderr, proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + (
            f"\nStopped after {RUN_TIMEOUT}s. Servers (uvicorn) and endless loops "
            "should run in your terminal instead."
        )
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        code, timed_out = None, True
    elapsed = time.perf_counter() - start

    images = []
    for png in sorted(fig_dir.glob("*.png")):
        images.append(base64.b64encode(png.read_bytes()).decode())
    shutil.rmtree(fig_dir, ignore_errors=True)

    return {
        "stdout": stdout[-50_000:],
        "stderr": stderr[-50_000:],
        "returncode": code,
        "timed_out": timed_out,
        "seconds": round(elapsed, 3),
        "images": images,
        "python": sys.executable,
    }


class CheckIn(BaseModel):
    day: str
    name: str
    code: str


CHECK_MARK = "@@BENCH_CHECKS@@"


@app.post("/api/check")
def check(body: CheckIn):
    """Save the file, run it, then run its check script. Returns one result per check."""
    if not DAY_RE.match(body.day):
        raise HTTPException(400, "Invalid day folder.")
    checks = check_path(body.day, body.name)
    if not checks.exists():
        raise HTTPException(404, "This file has no checks.")
    target = safe_path(body.day, body.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.code, encoding="utf-8")

    env = {**os.environ, "MPLBACKEND": "Agg", "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"}
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "checker.py"), str(target), str(checks)],
            cwd=target.parent, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=RUN_TIMEOUT, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"results": [{"label": "Checks finished in time", "ok": False,
                             "detail": f"Stopped after {RUN_TIMEOUT}s.",
                             "hint": "Look for an endless loop, or code that waits for a server."}],
                "seconds": RUN_TIMEOUT}
    elapsed = round(time.perf_counter() - start, 3)

    payload = None
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith(CHECK_MARK):
            payload = json.loads(line[len(CHECK_MARK):])
            break
    if payload is None:
        return {"results": [{"label": "Checks ran", "ok": False,
                             "detail": (proc.stderr or proc.stdout)[-3000:] or "No result from the checker."}],
                "seconds": elapsed}
    return {"results": payload["results"], "stdout": payload.get("stdout", ""),
            "stderr": proc.stderr[-5000:], "seconds": elapsed}


if __name__ == "__main__":
    import uvicorn

    LAB_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n  Bench is running at http://127.0.0.1:{PORT}")
    print(f"  Lab folder: {LAB_DIR}")
    print(f"  Python:     {sys.executable}\n")
    threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
