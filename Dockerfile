# Production Docker image for Dictionary Bot
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ src/
COPY pyproject.toml .
COPY README.md .

# Install package in editable mode
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 botuser
USER botuser

# Default: run interactive chatbot
# Pass OPENAI_API_KEY as env var or mount a .env file
ENTRYPOINT ["python", "-m", "dictionary_bot"]
