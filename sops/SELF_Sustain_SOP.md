# SOP-04: Self-Sustaining & Replication Protocol
**Objective:** Ensure 99.9% uptime and zero-manual-intervention replication.

1. **Integrity Monitoring:**
   - Every 5 minutes, verify the presence of core files: `.env`, `docker-compose.yml`, `core_orchestrator.py`.
   - If a file is missing/corrupted, pull the "Golden Copy" from the `/backup` directory.

2. **State Persistence:**
   - Database backups must be performed every 6 hours.
   - Vector Memory (ChromaDB) must be persisted to the `/memory` volume to survive container restarts.

3. **Replication Standards:**
   - The "Company in a Box" must be stripped of the owner's `OLLAMA_URL`, `STRIPE_KEYS`, and `DATABASE_PASSWORDS`.
   - Replace these with placeholder environment variables in a `.env.example` file.
   - The package must include a `bootstrap.bat` script for the end-user to run on Windows.

4. **Self-Scheduling:**
   - The system must autonomously schedule its own "Code Cleanup" and "Memory Optimization" tasks during low-usage hours.