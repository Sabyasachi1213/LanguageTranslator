@echo off
REM Double-click this file if you see a "'...' is not installed" error.
REM It installs torch AND everything else in requirements.txt for the
REM SAME Python that runs app.py, checks them, then starts the app.
REM Do not close this window while it is installing - it takes a few minutes.
echo Installing torch and the other packages... please wait, do not close this window.
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
  echo.
  echo Torch install failed. Please run this file again, or send a screenshot of the error above.
  pause
  exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Install failed. Please run this file again, or send a screenshot of the error above.
  pause
  exit /b 1
)
python -c "import torch, IndicTransToolkit, transformers; print('All packages OK:', torch.__version__)"
if errorlevel 1 (
  echo.
  echo A package is still missing for this Python. Send a screenshot of this window.
  pause
  exit /b 1
)
echo.
echo Everything is installed. Starting the translator at http://localhost:5004
python app.py
pause
