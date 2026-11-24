"""Government English -> Hindi Translator. Run: python app.py

One file does everything: loads the IndicTrans2 model and serves the
web page at http://localhost:5004

The default model is gated on Hugging Face: you must accept its
licence and log in with a token (see README, "Hugging Face access").
Put the token in a file called .env next to app.py, like this:
    HF_TOKEN=hf_your_token_here
Never share that token. The app reads it only to download the model.

For a live demo that needs no login at all, set MODEL_NAME to the
public model Helsinki-NLP/opus-mt-en-hi instead (see README, "Live").
"""
import os
import re

from flask import Flask, jsonify, request, send_from_directory

MODEL = os.environ.get(
    "MODEL_NAME", "ai4bharat/indictrans2-en-indic-dist-200M"
)
# Hugging Face Spaces sets PORT=7860; locally it defaults to 5004.
PORT = int(os.environ.get("PORT", "5004"))
# Only IndicTrans2 needs IndicTransToolkit. Public MarianMT models
# (e.g. Helsinki-NLP/opus-mt-en-hi) translate without it.
USE_INDIC = "indictrans" in MODEL.lower()

GOVERNMENT_TERMS = [
    "government", "ministry", "citizen", "scheme", "policy",
    "certificate", "application", "department", "services", "official",
]

# The model is loaded only when you translate for the first time,
# so the web page opens fast. First translation downloads ~1.1 GB.
_model = None
_tokenizer = None
_processor = None
_device = "cpu"


def _get_hf_token():
    """Read HF_TOKEN from the environment, or from a .env file."""
    token = os.environ.get("HF_TOKEN", "").strip()
    if token:
        return token
    env_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".env"
    )
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("HF_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


GATED_MESSAGE = (
    "This model is gated on Hugging Face, and your account has not "
    "been given access yet (or you are not logged in).\n"
    "1. Create a free account at https://huggingface.co, then open\n"
    "   https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M\n"
    "   and click Agree / Request access.\n"
    "2. Create a token at https://huggingface.co/settings/tokens\n"
    "   (type: Read).\n"
    "3. In the miniPRJ folder, copy .env.example to .env and put\n"
    "   HF_TOKEN=hf_your_token_here in it. Never share the token.\n"
    "4. Restart the app: python app.py"
)


def load_model():
    """Load the model once. Gives a clear error if torch is missing."""
    global _model, _tokenizer, _processor, _device
    if _model is not None:
        return

    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        if USE_INDIC:
            from IndicTransToolkit import IndicProcessor
    except ModuleNotFoundError as e:
        missing = e.name or "torch"
        # Tell the user to install the package that is actually missing.
        # Torch is the only one with a special install command.
        if missing == "torch":
            command = (
                "python -m pip install torch --index-url "
                "https://download.pytorch.org/whl/cpu"
            )
        else:
            command = "python -m pip install -r requirements.txt"
        raise RuntimeError(
            f"'{missing}' is not installed for this Python yet. "
            "Close the app and run this one command in PowerShell, "
            "in the miniPRJ folder, then start it again:\n" + command
        ) from e

    token = _get_hf_token()
    try:
        if token:
            from huggingface_hub import login

            login(token=token)
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL, trust_remote_code=True, token=token
        )
        _processor = IndicProcessor(inference=True) if USE_INDIC else None
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL, trust_remote_code=True, token=token
        ).to(_device)
        _model.eval()
    except Exception as e:
        text = str(e).lower()
        if "gated" in text or "401" in text or "must have access" in text:
            raise RuntimeError(GATED_MESSAGE) from e
        raise


def translate_to_hindi(text):
    """Translate English text to Hindi (same settings as the notebook)."""
    load_model()
    import torch

    # Translate sentence by sentence, so long text is not cut off.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip())
                 if s.strip()]
    out = []
    for sentence in sentences:
        if USE_INDIC:
            batch = _processor.preprocess_batch(
                [sentence], src_lang="eng_Latn", tgt_lang="hin_Deva"
            )
        else:
            batch = [sentence]
        inputs = _tokenizer(
            batch, truncation=True, padding="longest",
            return_tensors="pt", return_attention_mask=True,
        ).to(_device)
        with torch.no_grad():
            tokens = _model.generate(
                **inputs, use_cache=False, max_length=256, num_beams=5,
                num_return_sequences=1,
            )
        decoded = _tokenizer.batch_decode(
            tokens.detach().cpu(), skip_special_tokens=True
        )
        if USE_INDIC:
            decoded = _processor.postprocess_batch(decoded, lang="hin_Deva")
        out.append(decoded[0])
    return " ".join(out)


def count_sentences(text):
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])


app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok", "model": MODEL,
        "device": _device, "model_loaded": _model is not None,
    })


@app.route("/api/translate", methods=["POST"])
def translate_api():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "").strip()
    if not text:
        return jsonify({"hindi_translation": "", "sentence_count": 0,
                        "terms_detected": []})
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 characters)."}), 400
    try:
        hindi = translate_to_hindi(text)
    except Exception as e:  # show the clear message in the web page
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "hindi_translation": hindi,
        "sentence_count": count_sentences(text),
        "terms_detected": [t for t in GOVERNMENT_TERMS if t in text.lower()],
    })


if __name__ == "__main__":
    _names = ["torch", "transformers"]
    if USE_INDIC:
        _names.append("IndicTransToolkit")
    _missing = []
    for _name in _names:
        try:
            __import__(_name)
        except ModuleNotFoundError:
            _missing.append(_name)
    if _missing:
        print(f"WARNING: not installed for this Python yet: {', '.join(_missing)}.")
        print("Run: python -m pip install -r requirements.txt")
        print("The web page will still open, but translation will fail "
              "until they are installed.\n")
    if USE_INDIC and not _get_hf_token():
        print("NOTE: no HF_TOKEN found. This model is gated, so you will")
        print("need one — see README, 'Hugging Face access'.\n")
    print(f"Model: {MODEL}")
    print(f"Open http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)
