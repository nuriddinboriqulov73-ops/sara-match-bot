# Sara Match Bot - Docker Container

FROM python:3.9-slim

# Working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY sara_match_bot.py .
COPY advanced_features.py .

# Environment variable uchun
ENV BOT_TOKEN=""

# Bot ishga tushirish
CMD ["python", "sara_match_bot.py"]
