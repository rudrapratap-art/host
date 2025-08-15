FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

# Install system deps (ffmpeg often required for media bots/yt_dlp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps (requirements.txt is inside pyrogram-bot-render/)
COPY pyrogram-bot-render/requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy application code from the subfolder
COPY pyrogram-bot-render/ .

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "src/newfile.py"]