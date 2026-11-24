# miniPRJ — Government English → Hindi Translator

Translates government English text into Hindi, in your browser.

**Example**

> "The Government of India provides various services to citizens."
> → "भारत सरकार नागरिकों को विभिन्न सेवाएं प्रदान करती है।"

Default model: `ai4bharat/indictrans2-en-indic-dist-200M`
(IndicTrans2, from the original notebook). It translates sentence by
sentence, and highlights government terms it finds, such as
government, ministry, citizen, scheme, policy, certificate,
application, department, services and official.

**Live demo:** https://languagetranslator-weaenvdnxfpgoxgvqxhaxi.streamlit.app/
— anyone can open it and translate, no login needed. Tested 2026-11-25: live translation verified.
See [Live — open for everyone](#live--open-for-everyone) below.

---

## Who is this guide for?

Anyone — even if you have **never used Python, pip, VS Code, or a
terminal before**.

You do **not** need VS Code. You do **not** need to know how to code.
You only need:

- A Windows, Mac, or Linux computer
- Internet (the first translation downloads the model, about 1.1 GB)
- About 2 GB of free disk space
- A web browser (Chrome, Edge, Firefox, Safari — any of them)
- About 10–15 minutes for the first setup

Python is needed, but Step 1 below installs it for you, with pip
included. `pip` is just Python's installer for extra packages — you
do not need to install it separately.

---

## Step 0 — Get the project

**Option A — Download (easiest, no Git needed):**

1. On the GitHub page for this project, click the green **Code**
   button, then **Download ZIP**.
2. Find the downloaded `LanguageTranslator-main.zip` (usually in Downloads).
3. Right-click it and choose **Extract All** (Windows) or
   double-click it (Mac). You will get a folder called `LanguageTranslator`.

**Option B — With Git (if you already have Git):**

```bash
git clone https://github.com/Sabyasachi1213/LanguageTranslator.git
cd LanguageTranslator
```

> The exact GitHub link will be the link for this repository.
> If you downloaded the ZIP, skip Option B.

---

## Step 1 — Install Python (only once)

Python 3.12 or 3.13 is recommended. Python 3.14 also works with
this version of the project (see
[Troubleshooting: Python 3.14](#python-314--numpy-error) below).

### Windows

1. Go to https://www.python.org/downloads/
2. Click **Download Python** (the big yellow button) and run the
   installer you downloaded.
3. **Very important:** on the first installer screen, tick the box
   **"Add python.exe to PATH"** at the bottom, *before* you click
   Install. If you miss this, the commands later will say
   `'python' is not recognized`.
4. Click **Install Now**, wait for it to finish, then close the
   installer.
5. Check it worked. Open PowerShell (see Step 2) and run:

   ```powershell
   python --version
   python -m pip --version
   ```

   You should see something like `Python 3.13.5` and a pip version.
   If you see an error instead, close PowerShell, open it again,
   and try once more. If it still fails, reinstall Python and
   tick **Add python.exe to PATH** again.

### Mac

1. Go to https://www.python.org/downloads/macos/ and download the
   installer for your Mac, then run it.
2. Check it worked. Open Terminal and run:

   ```bash
   python3 --version
   python3 -m pip --version
   ```

   On a Mac, use `python3` (not `python`) in every command in
   this guide.

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
python3 -m pip --version
```

---

## Step 2 — Open a terminal in the project folder

You do not need VS Code for this. Use the terminal that is already
on your computer.

### Windows

1. Open the `LanguageTranslator` folder in File Explorer.
2. Click the address bar at the top of the File Explorer window
   (where it shows the folder path), type `powershell`, and press
   Enter. A blue PowerShell window opens, already in that folder.
3. Check you are in the right place by running:

   ```powershell
   dir
   ```

   You should see `app.py`, `requirements.txt`, `setup.bat`
   and the other files listed.

### Mac / Linux

1. Open Terminal.
2. Go into the folder, for example:

   ```bash
   cd ~/Downloads/LanguageTranslator
   ```

3. Check with `ls` — you should see `app.py`,
   `requirements.txt`, `setup.sh` and the other files.

---

## Step 3 — Install everything and start the app

### Windows — easiest way

In the `LanguageTranslator` folder, **double-click `setup.bat`**.

That one file does everything: it installs all the packages, checks
that torch is installed, then starts the app. Wait until it says
"Step 2 of 2" and "Starting the translator at
http://localhost:5004". Installing takes a few minutes the first
time. **Do not close the window early.**

### Mac / Linux — easiest way

In Terminal, in the `LanguageTranslator` folder, run:

```bash
bash setup.sh
```

Wait for the same "Step 2 of 2" message. Do not close Terminal early.

### If you prefer to type the commands yourself

Windows (PowerShell, in the `LanguageTranslator` folder):

```powershell
python -m pip install -r requirements.txt
python app.py
```

Mac / Linux (Terminal, in the `LanguageTranslator` folder):

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Use `python -m pip` (Windows) or `python3 -m pip` (Mac/Linux) —
**not plain `pip`**. Plain `pip` can install packages for a
different Python than the one that runs `app.py`, and then the app
says a package "is not installed" even though you installed it.

Wait for the first command to say **"Successfully installed"**.
Do not close the window early — it takes a few minutes.

---

## Step 4 — Hugging Face access (do this before the first translation)

The default model is **gated** on Hugging Face. Hugging Face will
not let you download it until your account has accepted its licence
and logged in. That is why you get a `401 / gated repo` error
without these steps. The original notebook worked because its
owner had already done this.

Do these 4 steps, in order:

1. **Create a free account** at https://huggingface.co
2. **Accept the model licence.** Open
   https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M
   and click **Agree** / **Request access**.
   Do this on the **Model card** tab — there is nothing to do on
   the **Community** tab. Make sure you are logged in (your name
   or picture should show at the top right).
3. **Create a token.** Go to https://huggingface.co/settings/tokens
   and create a token of type **Read**. Copy it — you will only
   see it once.
4. **Put the token in a `.env` file** (local only — see below).
   In the `LanguageTranslator` folder, copy `.env.example` to a new file
   called `.env`, and replace `hf_your_token_here` with your token:

   ```text
   HF_TOKEN=hf_your_token_here
   ```

   Windows (PowerShell, in the `LanguageTranslator` folder):

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Then replace `hf_your_token_here` with your token, save with
   Ctrl+S, close Notepad, and restart the app with `python app.py`.

   Mac / Linux (Terminal, in the `LanguageTranslator` folder):

   ```bash
   cp .env.example .env
   ```

   Then open `.env` in any text editor, replace
   `hf_your_token_here` with your token, save, and restart the
   app with `python3 app.py`.

If you skip step 2, the token alone will still give a 401 error.

### About `.env` — read this

- `.env` is **for local use only, on your own computer**.
- **Never share your token.** Never put it in the code, in GitHub,
  in a chat message, or in a screenshot.
- **Never commit `.env`.** It is already in `.gitignore`, so Git
  will not upload it.
- `.env.example` is only a template. It contains the placeholder
  `hf_your_token_here`, not a real token. **Never put a real token
  in `.env.example`** — that file *is* published on GitHub.
- If a token ever leaks (for example, you pasted it somewhere
  public), delete it at https://huggingface.co/settings/tokens
  and create a new one.

### No token? Use the public model instead

If you do not want to create a Hugging Face account at all, run
the app with the public Helsinki model instead. It needs **no
token and no licence step**, and anyone can use it:

Windows (PowerShell, in the `LanguageTranslator` folder):

```powershell
$env:MODEL_NAME = "Helsinki-NLP/opus-mt-en-hi"
python app.py
```

Mac / Linux (Terminal, in the `LanguageTranslator` folder):

```bash
MODEL_NAME=Helsinki-NLP/opus-mt-en-hi python3 app.py
```

`MODEL_NAME` is an environment setting for that one run — it is
not read from `.env`, so set it in the terminal each time you
start the app this way. Translation quality is different from
IndicTrans2, but it works with no login.

---

## Step 5 — Translate

1. With the app running, open your browser and go to
   **http://localhost:5004**
2. Type or paste English text in the box, for example:
   "The Government of India provides various services to citizens."
3. Click **Translate to Hindi**.
4. The Hindi translation appears below, along with the sentence
   count and any government terms detected.

The first translation downloads the model (about 1.1 GB for
IndicTrans2) and can take a few minutes — in testing, the first
Helsinki translation took about 2 minutes, and later ones took
about 4 seconds because the model was already downloaded. The
web page itself opens fast, because the model is only loaded when
you translate for the first time. The server takes about 10
seconds to start.

To stop the app, go back to the terminal window and press
**Ctrl+C**. To start it again, run `python app.py` (Windows) or
`python3 app.py` (Mac/Linux) in the `LanguageTranslator` folder.

---

## What the files are

- `app.py` — the app (reads `MODEL_NAME`, `PORT` and `HF_TOKEN`)
- `index.html` — the web page
- `requirements.txt` — what to install (torch, transformers,
  IndicTransToolkit, Flask, sentencepiece, numpy)
- `.env.example` — copy to `.env` and add your Hugging Face token
- `Dockerfile` — for Hugging Face Spaces / Docker
- `.dockerignore` — keeps `.env`, `.venv` and `__pycache__` out
  of the Docker image
- `.gitignore` — keeps `.venv`, `.env` and model files out of GitHub
- `LICENSE` — MIT
- `setup.bat` / `setup.sh` — install + start in one go
- `fix-torch.bat` — installs torch + everything else, then starts
  the app (Windows, see Troubleshooting)

### Sharing the project

You do **not** need to share the whole folder. The installed
packages (`.venv`) and the downloaded model are what make the
folder huge — over 10 GB. The actual project code is only about
20 KB.

- **`.venv` is not required.** It is just your local copy of the
  installed packages. You can delete it, and anyone else will
  install the same packages again from `requirements.txt`.
  Deleting `.venv` does not break the project — run `setup.bat`
  (or `setup.sh`) again to reinstall what you need.
- When you share the project, share only the source files:
  `app.py`, `index.html`, `requirements.txt`, `README.md`,
  `setup.bat`, `setup.sh`, `fix-torch.bat`, `.env.example`,
  plus `.gitignore`, `Dockerfile`, `.dockerignore` and `LICENSE`.
- **Never** include `.venv`, `__pycache__`, `.env`, or downloaded
  model files.

---

## API (for developers)

The web page uses this API, and you can use it too:

- `GET /` — the web page
- `GET /api/health` — `{"status": "ok", "model": "...",
  "device": "cpu", "model_loaded": true/false}`
- `POST /api/translate` with `{"text": "..."}` — returns
  `{"hindi_translation": "...", "sentence_count": 1,
  "terms_detected": ["government", "citizen", "services"]}`

Example (PowerShell):

```powershell
Invoke-RestMethod -Uri http://localhost:5004/api/translate `
  -Method Post -ContentType "application/json" `
  -Body '{"text": "The Government of India provides various services to citizens."}'
```

---

## Live — open for everyone

GitHub alone cannot run this app: GitHub Pages only serves static
pages, and this needs Python + the model.

**Hugging Face Spaces is no longer free for this:** as of
2026-11-25, only the Static SDK is free on Hugging Face Spaces —
Docker, Gradio and Streamlit Spaces are paid. Static cannot run
Python or Flask, so it cannot run this app. **Do not pay for a
Space.**

The free live version runs on **Streamlit Community Cloud**
(free for public apps, deploys straight from GitHub):

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** / **Deploy an app**.
3. Choose:
   - Repository: `Sabyasachi1213/LanguageTranslator`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
4. Click **Deploy**. The first build takes a few minutes.
5. Streamlit gives you a public link, like
   `https://languagetranslator-xxxx.streamlit.app`. Anyone can
   open that link and translate — they do not need an account.

That live app uses the public Helsinki model
(`Helsinki-NLP/opus-mt-en-hi`) by default, so it needs no token
and no Hugging Face licence step. Translation quality is
different from IndicTrans2, but anyone can try it with no login.
The Flask app (`app.py`) stays the default locally, with
IndicTrans2.

Notes:
- Streamlit apps sleep after about 12 hours with no traffic,
  and wake up again when someone visits. The first translation
  after waking up downloads the model again, so it can take a
  couple of minutes.
- To use IndicTrans2 on Streamlit instead, set `MODEL_NAME` to
  `ai4bharat/indictrans2-en-indic-dist-200M` and add `HF_TOKEN`
  as a secret in Streamlit Cloud (Settings → Secrets). Never
  put the token in the code or in GitHub. That model is gated,
  so it also needs licence access on Hugging Face.

**Live demo:** https://languagetranslator-weaenvdnxfpgoxgvqxhaxi.streamlit.app/
— anyone can open it and translate, no login needed. Tested 2026-11-25: live translation verified.

---

## Troubleshooting

### `'python' is not recognized` / `'pip' is not recognized`

Python is not on your PATH. Reinstall Python from
https://www.python.org/downloads/ and tick **"Add python.exe to
PATH"** on the first installer screen. Then close the terminal
completely, open a new one, and try again.

### `No module named 'torch'` / `'...' is not installed`

That means a package was installed for a different Python, or the
install did not finish. Torch alone is not enough — you also need
IndicTransToolkit, transformers, Flask, sentencepiece and numpy.

- Easiest fix (Windows): double-click `fix-torch.bat`. It installs
  torch and everything else, checks them, then starts the app.
  Wait until it says the packages are OK.
- Or, in PowerShell / Terminal, in the `LanguageTranslator` folder, run this
  one command. Use `python -m pip`, not plain `pip`:

  ```powershell
  python -m pip install -r requirements.txt
  python app.py
  ```

- Wait for the first command to say "Successfully installed".
  Do not close the window early — it takes a few minutes.
- If it still names a missing package, send a screenshot of the
  first command's output (the install output, not just the error).

### `This tokenizer cannot be instantiated ... sentencepiece`

This was a bug in an earlier version: `sentencepiece` was missing
from `requirements.txt`, so the Helsinki / MarianMT tokenizer
failed. It is fixed in this version — `sentencepiece==0.2.3` is
now in `requirements.txt`. If you still see this error, you are
using an old copy: download the latest version from GitHub and
run `python -m pip install -r requirements.txt` again, then
restart the app.

### Python 3.14 / numpy error

If you are on Python 3.14, the old `numpy==2.1.3` pin broke the
install: numpy 2.1.3 has no ready-made wheel for Python 3.14, so
pip tries to build it from source and fails with a Meson /
`complex.h` error ("complex.h header does not include complex
type complex float"). That failure also stops `IndicTransToolkit`
from installing.

This version fixes it by letting pip pick a newer numpy
(`numpy>=2.3`, pip now picks 2.5.5 as a wheel). Do not change it
back to `numpy==2.1.3`.

### `401 / gated repo` error

See [Step 4 — Hugging Face access](#step-4--hugging-face-access-do-this-before-the-first-translation).
You need **both**: (1) accept the licence on the model page
(Model card tab, while logged in), **and** (2) a Read token in
`.env`. A token alone, without the licence step, still gives 401.
If the model page still shows "Request access", the licence step
is not done yet.

The app shows this as a plain-language message, not the raw 401.

### First translation is very slow / download fails

The first translation downloads the model, so it is slow — that
is normal. In testing, the first Helsinki translation took about
2 minutes, and later ones took about 4 seconds. If the download
fails with a connection / proxy error, check your internet and
try again — the app does not retry a failed download by itself.
Just click Translate again.

### The page will not open at http://localhost:5004

- Check the terminal window: it should say
  "Open http://localhost:5004". If it does not, the app has not
  started yet — wait a few seconds, or scroll up for an error.
- Make sure you did not close the terminal window — closing it
  stops the app.
- If another copy of the app is already running, stop it with
  Ctrl+C in its terminal window first, then start it again.

### The app opens, but translation fails

Look at the terminal window for the error message — that is the
real error, and the web page shows the same message. Take a
screenshot of the terminal, including the first error lines.

---

## Tested

Tested on 2026-11-24 in a clean install (Python 3.12.3):

- `py_compile` passed.
- Install succeeded in about 1 minute 30 seconds: torch
  2.15.0+cpu, transformers 4.57.6, IndicTransToolkit 1.1.1,
  Flask 3.1.3, numpy 2.5.5, huggingface-hub 0.36.2,
  sentencepiece 0.2.3.
- `GET /`, `GET /api/health` and empty translate: 200.
- IndicTrans2 with no token: gated 401 in 3 seconds, with the
  friendly message above (not the raw 401).
- Helsinki model, no token: worked. "The Government of India
  provides various services to citizens." →
  "भारत की सरकार नागरिकों को विभिन्न सेवाएँ प्रदान करती है ।"
  (4 seconds once cached; 118 seconds on first load).
- "The Ministry has launched a new scheme for farmers." →
  "मंत्रालय ने किसानों के लिए एक नयी योजना शुरू की है।"

Real IndicTrans2 translation can only be tested by someone whose
Hugging Face account has accepted the model licence and has a
token — the model download itself is gated.

## License

MIT — see `LICENSE`.
