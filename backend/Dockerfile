# ==============================================================================
# SOVEREIGN SDK: BACKEND & MONITOR DOCKERFILE
# Version: 1.0.2-Alpha
# Description: Fixed CMD syntax to resolve build context parse error.
# ==============================================================================
FROM python:3.11-slim

# SRE HARDENING PROTOCOLS
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    sqlite3 \
    libsqlite3-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/output/src && chmod -R 777 /app/output

EXPOSE 8000

# FIX: Added space between CMD and bracket to prevent parse failure
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]