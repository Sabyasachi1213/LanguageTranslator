# For Hugging Face Spaces (Docker SDK) and any Docker host.
# HF Spaces sets PORT=7860 automatically; app.py reads PORT from the
# environment, so the same image works locally on port 5004 too.
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=7860
EXPOSE 7860
CMD ["python", "app.py"]
