#!/bin/bash
# 1. Clean the 'incorrect label' network
docker network rm swarm_network 2>/dev/null || true

# 2. Re-sync Laptop Brain
GATEWAY_IP=$(ip route | grep default | awk '{print $3}')
sed -i "s|OLLAMA_URL=.*|OLLAMA_URL=http://$GATEWAY_IP:11434|g" .env

# 3. Production build using the Linux Socket
DOCKER_HOST=unix:///var/run/docker.sock docker compose up -d --build

echo "Factory infrastructure stabilized. Monitoring backend..."
sleep 5
docker logs -f swarmenterprise-backend-1
