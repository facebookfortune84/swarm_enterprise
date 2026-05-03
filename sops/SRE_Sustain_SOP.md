# SOP-08: SITE RELIABILITY & SELF-SUSTENANCE PROTOCOL

## 1. PURPOSE
This protocol defines the autonomous maintenance standards for the Swarm Enterprise ecosystem. It ensures the 'Will to Live' of the factory by mandating continuous health checks, automated service recovery, and the preservation of the core file system.

## 2. THE MONITORING HIERARCHY
The **SRE Agent** oversees the **Swarm Monitor** service. 
- **L1 (Process):** Monitoring individual agent execution timeouts (Default: 600s).
- **L2 (Container):** Monitoring the status of the 6 core Docker services.
- **L3 (Integrity):** Monitoring the physical existence of the Constitution (SOPs) and the .env file.

## 3. PROCEDURES: SELF-HEALING (CONTAINER LAYER)
The Monitor service must query the Docker Socket (\`/var/run/docker.sock\`) every 60 seconds.
1. **Detection:** If any service (\`backend\`, \`tunnel\`, \`chromadb\`, etc.) is in a status other than 'Running'.
2. **Action:** Issue a \`docker start [container_id]\` command.
3. **Escalation:** If the service fails to start 3 times, the SRE must trigger a \`docker compose up -d --build [service_name]\` to re-pull the image and reset the state.

## 4. PROCEDURES: FILE SYSTEM INTEGRITY (THE REPLICATOR GATE)
To ensure the 'Company in a Box' remains saleable, the file system must never rot.
1. **Verification:** Every 24 hours, the SRE must run a SHA-256 scan on the \`/app/sops/\` and \`/app/backend/core/\` directories.
2. **Golden Copy:** If a file is missing or the hash has changed without a verified 'Architect Ticket', the SRE must pull the 'Golden Copy' from the hidden \`/app/backup/\` volume.
3. **Restoration:** Physically overwrite the corrupted file and log a 'Security Breach' event in the Linear Engine.

## 5. RESOURCE OPTIMIZATION (CPU/RAM MANAGEMENT)
Since inference runs on the Laptop's 30GB RAM, the SRE must manage the 'Inference Debt'.
- **Zombie Kill:** Identify and kill any \`ollama_llama_server\` processes that have been idle for more than 1800 seconds.
- **Pruning:** Every Sunday at 03:00 AM, the Monitor must run \`docker system prune -f\` to clear old build cache and free up disk space for new builds.

## 6. BACKUP & PERSISTENCE
The system must maintain state across reboots.
- **Relational Memory:** Perform a \`VACUUM\` and snapshot of \`swarm_tickets.db\` every 12 hours.
- **Vector Memory:** Ensure ChromaDB commits all shards to the \`/app/memory_data/\` persistent volume before any scheduled maintenance.

## 7. AUTOMATED REPORTING
- **Heartbeat:** The SRE must update the \`/api/health\` endpoint status every 5 minutes.
- **Alerting:** In the event of a tunnel disconnect, the SRE must use the \`write_enterprise_file\` tool to create a \`CRITICAL_SYSTEM_ALERT.md\` in the project root to inform the owner.

## 8. COMPLETION CRITERIA
The Maintenance Cycle is considered 'SUCCESSFUL' only when:
1. All 6 containers report 'Healthy'.
2. The Laptop Brain returns a 200 OK on the \`/api/tags\` endpoint.
3. No unapproved file modifications are detected.