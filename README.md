# Bench

A local learning platform for your 12-week plan: lessons, a code editor, a Run button with output and plots, quizzes, notes, and progress tracking. Your code is saved as real files in `ml-fundamentals-lab/dayNN/`.

## Install (once)

1. Unzip so `bench` sits **next to** your lab folder:

   ```
   Documents/
   ├── bench/
   └── ml-fundamentals-lab/
   ```

2. Install the server packages into your lab's virtual environment:

   ```bash
   cd ml-fundamentals-lab
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # Mac/Linux
   pip install -r ../bench/requirements.txt
   ```

## Start

- **Windows:** double-click `start.bat`
- **Mac/Linux:** `./start.sh`
- **Or:** with your venv active, `cd bench` then `python server.py`

Your browser opens at http://127.0.0.1:8765. Stop it with Ctrl+C in the terminal.

Bench runs your code with the Python it was started with, so start it from your lab's `.venv` and every package you installed there (scikit-learn, matplotlib, httpx...) is available.

## How a day works

1. **Lesson tab:** read, and press **Run snippet** on any Python example to try it.
2. **Editor:** each day's exercise files open with instructions. Write the code yourself.
3. **Yellow box:** write your prediction before running. Run stays locked until you do (untick "Predict before running" to turn this off).
4. **Run** (or Ctrl+Enter): output, errors, and matplotlib plots appear below, next to your prediction. Each line of your prediction is marked ✓ or ✗ against the real output.
5. **Check** (or Ctrl+Shift+Enter): runs automatic checks on your exercise and lists what's correct and what's missing, with a hint for each miss. A ✓ appears on the file tab once every check passes.
6. **Tasks, Quiz, Notes:** tick tasks, take the 3-question check, and write your interview-style answer (saved to `notes.md`).
7. **Sunday:** the Re-test tab (10 questions, 8 to pass).

Ctrl+S saves (it also autosaves). **Reset to starter** restores a file's original instructions.

## Exercises and checks

Each exercise starts as a scaffold: the imports, function names and signatures are written for you, and every `...` marks a part you fill in. Docstrings say what each function must return.

Starters and checks live in `labs/dayNN/`:

```
labs/day01/defaults.py           starter shown in the editor
labs/day01/checks/defaults.py    what the Check button verifies
```

Check imports your file (code under `if __name__ == "__main__":` is skipped), then calls your functions and reads your variables, so keep the names from the starter. Files you started before checks existed keep your code; if a check says a name is missing, save your work elsewhere and press **Reset to starter**. Non-Python files (Dockerfile, YAML, README) are checked as text. See `checker.py` for the helpers a check script can use.

## Things to know

- **Servers:** Day 2 and Week 2 have FastAPI apps. Run those in a separate terminal with `uvicorn` (the lesson shows the command); Bench stops any script after 60 seconds. Change the limit with the `RUN_TIMEOUT` environment variable.
- **Internet:** the code editor and fonts load from a CDN. Offline, Bench falls back to a plain text editor; everything else still works.
- **Your files are never overwritten:** starter code is only written to files that are missing or empty.
- **Progress** lives in `bench/progress.local.json`, which git ignores, so switching branches or pulling never touches it. On first start it carries over anything in the old `progress.json`. Back it up if you like.
- **Different lab location:** set `LAB_DIR` before starting, e.g. `set LAB_DIR=D:\code\ml-fundamentals-lab` (Windows) or `export LAB_DIR=...` (Mac/Linux).
- **Safety:** Bench listens only on 127.0.0.1 and runs the code you write on your own machine. Don't expose it to a network.

## Next week's lessons

Weeks 3-12 show their goals and tasks. Each Sunday, tell Claude:

> Week N retro: here's what I finished and what slipped. Give me Week N+1's daily plan for Bench.

You'll get an updated `curriculum.py` plus that week's `labs/dayNN/` folders (starters and checks). Replace them and restart Bench. Your progress and code are kept.
