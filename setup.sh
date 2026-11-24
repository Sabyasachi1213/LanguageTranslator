#!/bin/bash
# Run: bash setup.sh — installs everything, then starts the app.
# Do not close the terminal while it is installing - it takes a few minutes.
set -e
cd "$(dirname "$0")"
echo "Step 1 of 2: Installing... please wait, do not close this window."
python3 -m pip install -r requirements.txt
if ! python3 -c "import torch" 2>/dev/null; then
  echo ""
  echo "Torch is still missing. Run this one command, then run bash setup.sh again:"
  echo "pip install torch --index-url https://download.pytorch.org/whl/cpu"
  exit 1
fi
echo ""
echo "Step 2 of 2: Starting the translator at http://localhost:5004"
python3 app.py
