FROM python:3.11-slim

# Install system-level diagnostic tools and network handlers
RUN apt-get update && apt-get install -y \\
    curl \\
    iputils-ping \\
    sqlite3 \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure into the container
# This ensures /agents and /sops are accessible to the Crew
COPY . .

# Expose the API port
EXPOSE 8000

# Start the Master Orchestrator with 4 worker threads for 40+ agents
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]