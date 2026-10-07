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

Each week is an **arena** and each day a **level**. The header shows the arena (click it for the map of all arenas) and the path of its levels; the step bar below shows where you are in today's level. Play the steps in order, using the Next button at the bottom of each one:

1. **Learn:** read the lesson on the left. The code editor on the right is a scratchpad: press **Try it in the editor** on any example to run it there, or type your own experiments. Finish with "I've read the lesson".
2. **Practice:** one exercise at a time. The left side explains the topic, your mission and the steps; the editor on the right holds the starter, guided by comments. Write your prediction in the yellow box, **Run** (Ctrl+Enter) to compare it line by line with the real output, then **Check** (Ctrl+Shift+Enter) to see what's right and what's missing.
3. **Quiz:** answer from memory; the scratchpad stays open if you want to verify something.
4. **Boss** (Sundays): the week's re-test, 8/10 to win.
5. **Missions:** everything that clears the level. Passing labs, writing notes and beating the boss tick their missions for you; tick the rest (reading, GitHub, applications) yourself. Links marked ↗ open where you do them.

**Notes** (button in the step bar) open in a side drawer and save to `notes.md`. Each level has three stars: lesson read, every lab passing, perfect quiz. **Hide ›** folds the editor away when you want the guide wider.

Ctrl+S saves (it also autosaves). **Reset to starter** restores an exercise's original scaffold.

## Exercises and checks

Each exercise starts as a scaffold: the imports, function names and signatures are written for you, and every `...` marks a part you fill in. Docstrings say what each function must return.

Starters and checks live in `labs/dayNN/`:

```
labs/day01/defaults.py           starter shown in the editor
labs/day01/briefs/defaults.md    the guided description shown beside it
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
