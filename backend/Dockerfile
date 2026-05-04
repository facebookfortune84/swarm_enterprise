FROM python:3.11-slim

# Install system-level diagnostic tools, build-essentials, AND python-dev
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    sqlite3 \
    libsqlite3-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Step-by-step copy to maximize Docker cache efficiency
COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy everything (agents, sops, etc)
COPY . .

EXPOSE 8000

# Start with 4 workers to handle the 12-manager hierarchy load
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
