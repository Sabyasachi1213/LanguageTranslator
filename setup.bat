@echo off
REM Double-click this file. It does everything, then starts the app.
REM Do not close this window while it is installing - it takes a few minutes.
echo Step 1 of 2: Installing... please wait, do not close this window.
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Install did not finish. Please run this file again.
  pause
  exit /b 1
)
python -c "import torch" 2>nul
if errorlevel 1 (
  echo.
  echo Torch is still missing. Run this one command, then run this file again:
  echo python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
  pause
  exit /b 1
)
echo.
echo Step 2 of 2: Starting the translator at http://localhost:5004
python app.py
pause
