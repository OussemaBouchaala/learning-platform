"""Loads exercise starters and their checks from labs/<day folder>/.

    labs/day01/defaults.py           starter code shown in the editor
    labs/day01/checks/defaults.py    check script run by the Check button (optional)

Non-Python files keep their name and get `.py` added for the check:
    labs/day13/Dockerfile  ->  labs/day13/checks/Dockerfile.py
"""
from pathlib import Path

LABS = Path(__file__).resolve().parent / "labs"


def check_path(folder: str, name: str) -> Path:
    return LABS / folder / "checks" / (name if name.endswith(".py") else name + ".py")


def lab(folder: str, name: str) -> dict:
    """One editor file for a day: {"name", "starter", "has_check"}."""
    return {
        "name": name,
        "starter": (LABS / folder / name).read_text(encoding="utf-8"),
        "has_check": check_path(folder, name).exists(),
    }
