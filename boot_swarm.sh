#!/bin/bash
# ==============================================================================
# SOVEREIGN SDK: SWARM ENTERPRISE BOOTSTRAP & GITOPS DAEMON
# Version: 1.0.1-Alpha
# Description: Initializes the fractal swarm, syncs the LLM gateway, and
#              starts the automated GitOps state synchronization loop.
# ==============================================================================

# STRICT MODE: Fail fast on errors, undefined variables, or pipeline failures.
set -euo pipefail

# TELEMETRY: Error trapping
error_handler() {
    echo "[!] CRITICAL ERROR: Boot sequence failed at line $1."
    echo "[!] Check Swarm OS Operational Protocols for debugging steps."
    exit 1
}
trap 'error_handler $LINENO' ERR

echo "[*] INITIATING SWARM OS BOOT SEQUENCE..."

# 1. CLEAN THE NETWORK PERIMETER
echo "[*] Step 1: Sanitizing Docker network state..."
docker network rm swarm_network 2>/dev/null || true

# 2. RE-SYNC LAPTOP BRAIN (OLLAMA GATEWAY)
echo "[*] Step 2: Synchronizing LLM Gateway via WSL2 Bridge..."
# Extracts the dynamic Windows Host IP from the WSL2 routing table
GATEWAY_IP=$(ip route | grep default | awk '{print $3}')
if [ -z "$GATEWAY_IP" ]; then
    echo "[!] WARNING: Could not determine Gateway IP. Defaulting to host.docker.internal"
    GATEWAY_IP="host.docker.internal"
fi
echo "[*] Gateway IP identified as: $GATEWAY_IP"

# Update the .env file securely
if [ -f .env ]; then
    sed -i "s|^OLLAMA_URL=.*|OLLAMA_URL=http://$GATEWAY_IP:11434|g" .env
    echo "[*] .env file updated with current inference brain gateway."
else
    echo "[!] WARNING: .env file not found. Skipping OLLAMA_URL injection."
fi

# 3. GITOPS STATE SYNCHRONIZATION DAEMON (BACKGROUND)
echo "[*] Step 3: Initializing GitOps State Sync Daemon..."
gitops_daemon() {
    while true; do
        sleep 3600 # 60 minute interval
        echo "[*] [GITOPS] Initiating scheduled state synchronization..."
        if [ -d ".git" ]; then
            git add . || true
            # Only commit if there are changes detected
            if ! git diff-index --quiet HEAD --; then
                TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S %Z")
                git commit -m "Auto-State Sync: $TIMESTAMP [Swarm OS]" || true
                git push origin main || echo "[!] [GITOPS] Push failed. Check network or remote configuration."
                echo "[*] [GITOPS] State synchronized and archived."
            else
                echo "[*] [GITOPS] No state changes detected. Skipping commit."
            fi
        else
            echo "[!] [GITOPS] Not a git repository. Skipping sync."
        fi
    done
}

# Launch daemon in background
gitops_daemon &
GITOPS_PID=$!
echo "[*] GitOps Daemon running in background (PID: $GITOPS_PID)."

# 4. SWARM FACTORY IGNITION
echo "[*] Step 4: Igniting Docker Swarm Factory..."
# Leveraging local linux socket explicitly to enforce WSL daemon routing
DOCKER_HOST=unix:///var/run/docker.sock docker compose up -d --build

echo "====================================================================="
echo "[+] FACTORY INFRASTRUCTURE STABILIZED & ONLINE"
echo "[+] GitOps Version Control: ACTIVE (60m intervals | PID: $GITOPS_PID)"
echo "[+] Inference Gateway: http://$GATEWAY_IP:11434"
echo "====================================================================="
echo "[*] Monitoring backend telemetry..."

# Allow containers to initialize before tailing logs
sleep 5
DOCKER_HOST=unix:///var/run/docker.sock docker logs -f swarmenterprise-backend-1