FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# OpenClaw workspace
RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

# Start Ollama once and pull model
RUN ollama serve & sleep 10 && ollama pull mistral

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Start BOTH Ollama + FastAPI
CMD ollama serve & python -u run.py
