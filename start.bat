@echo off
REM Starts Bench using the ml-fundamentals-lab virtual environment.
cd /d "%~dp0"
if exist "..\ml-fundamentals-lab\.venv\Scripts\python.exe" (
  "..\ml-fundamentals-lab\.venv\Scripts\python.exe" server.py
) else (
  python server.py
)
pause
