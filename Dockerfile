FROM python:3.12-slim

# Install dependensi sistem untuk audio & grafis
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libgl1 \
    libasound2 \
    libpulse0 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pustaka Python game
RUN pip install --no-cache-dir pygame-ce pytmx