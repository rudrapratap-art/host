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

# Install Python deps
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Create non-root user and switch
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Default command: run the bot. Adjust if your Procfile/render.yaml uses a different command
CMD ["python", "bot.py"]

# Python
# (Moved ignore patterns to .dockerignore file)