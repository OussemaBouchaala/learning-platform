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
4. **Run** (or Ctrl+Enter): output, errors, and matplotlib plots appear below, next to your prediction.
5. **Tasks, Quiz, Notes:** tick tasks, take the 3-question check, and write your interview-style answer (saved to `notes.md`).
6. **Sunday:** the Re-test tab (10 questions, 8 to pass).

Ctrl+S saves (it also autosaves). **Reset to starter** restores a file's original instructions.

## Things to know

- **Servers:** Day 2 and Week 2 have FastAPI apps. Run those in a separate terminal with `uvicorn` (the lesson shows the command); Bench stops any script after 60 seconds. Change the limit with the `RUN_TIMEOUT` environment variable.
- **Internet:** the code editor and fonts load from a CDN. Offline, Bench falls back to a plain text editor; everything else still works.
- **Your files are never overwritten:** starter code is only written to files that are missing or empty.
- **Progress** lives in `bench/progress.json`. Back it up if you like.
- **Different lab location:** set `LAB_DIR` before starting, e.g. `set LAB_DIR=D:\code\ml-fundamentals-lab` (Windows) or `export LAB_DIR=...` (Mac/Linux).
- **Safety:** Bench listens only on 127.0.0.1 and runs the code you write on your own machine. Don't expose it to a network.

## Next week's lessons

Weeks 3-12 show their goals and tasks. Each Sunday, tell Claude:

> Week N retro: here's what I finished and what slipped. Give me Week N+1's daily plan for Bench.

You'll get an updated `curriculum.py`. Replace the file and restart Bench. Your progress and code are kept.
