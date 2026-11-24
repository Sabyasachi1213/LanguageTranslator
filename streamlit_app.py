"""Streamlit version of miniPRJ — for the free live demo.

Run locally:  streamlit run streamlit_app.py
Deploy free:  Streamlit Community Cloud, from the GitHub repo,
              main file: streamlit_app.py

This uses the public Helsinki model by default, so it needs no
Hugging Face token and no licence step. Anyone can open the live
link and translate.

To use IndicTrans2 instead, set MODEL_NAME to
ai4bharat/indictrans2-en-indic-dist-200M and add HF_TOKEN as a
secret in Streamlit Cloud — that model is gated, so it also needs
licence access on Hugging Face. See README.md.
"""

import os
import re

import streamlit as st

MODEL = os.environ.get(
    "MODEL_NAME", "Helsinki-NLP/opus-mt-en-hi"
)
USE_INDIC = "indictrans" in MODEL.lower()

GOVERNMENT_TERMS = [
    "government", "ministry", "citizen", "scheme", "policy",
    "certificate", "application", "department", "services", "official",
]


def _get_hf_token():
    token = os.environ.get("HF_TOKEN", "").strip()
    if token:
        return token
    try:
        return st.secrets.get("HF_TOKEN", "").strip() or None
    except Exception:
        return None


@st.cache_resource(show_spinner="Loading the translation model — first time takes a couple of minutes…")
def load_model():
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    token = _get_hf_token()
    if token:
        from huggingface_hub import login

        login(token=token)
    processor = None
    if USE_INDIC:
        from IndicTransToolkit import IndicProcessor

        processor = IndicProcessor(inference=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL, trust_remote_code=True, token=token
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL, trust_remote_code=True, token=token
    ).to(device)
    model.eval()
    return model, tokenizer, processor, device


def translate_to_hindi(text):
    import torch

    model, tokenizer, processor, device = load_model()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip())
                 if s.strip()]
    out = []
    for sentence in sentences:
        if USE_INDIC:
            batch = processor.preprocess_batch(
                [sentence], src_lang="eng_Latn", tgt_lang="hin_Deva"
            )
        else:
            batch = [sentence]
        inputs = tokenizer(
            batch, truncation=True, padding="longest",
            return_tensors="pt", return_attention_mask=True,
        ).to(device)
        with torch.no_grad():
            tokens = model.generate(
                **inputs, use_cache=False, max_length=256, num_beams=5,
                num_return_sequences=1,
            )
        decoded = tokenizer.batch_decode(
            tokens.detach().cpu(), skip_special_tokens=True
        )
        if USE_INDIC:
            decoded = processor.postprocess_batch(decoded, lang="hin_Deva")
        out.append(decoded[0])
    return " ".join(out)


st.set_page_config(
    page_title="Government English → Hindi Translator",
    page_icon="🌐",
)
st.title("Government English → Hindi Translator")
st.write(
    "Translate government and official English text into Hindi. "
    "Type or paste text below and click **Translate to Hindi**."
)

text = st.text_area(
    "English text",
    value="The Government of India provides various services to citizens.",
    height=150,
)

if st.button("Translate to Hindi"):
    if not text.strip():
        st.warning("Please type some English text first.")
    else:
        try:
            with st.spinner("Translating… first time downloads the model, so please wait."):
                hindi = translate_to_hindi(text)
            st.subheader("Hindi translation")
            st.write(hindi)
            sentences = len([s for s in re.split(r"[.!?]+", text) if s.strip()])
            terms = [t for t in GOVERNMENT_TERMS if t in text.lower()]
            st.caption(f"Sentences: {sentences}  •  Terms detected: {', '.join(terms) if terms else 'none'}")
        except Exception as e:
            msg = str(e).lower()
            if "gated" in msg or "401" in msg or "must have access" in msg:
                st.error(
                    "This model is gated on Hugging Face. "
                    "Accept its licence at "
                    "https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M "
                    "and add a Read HF_TOKEN as a secret, then restart the app. "
                    "Or use the public Helsinki model, which needs no token."
                )
            else:
                st.error(f"Translation failed: {e}")

st.caption(f"Model: {MODEL}")
