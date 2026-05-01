# SOP-00: Board of Directors Governance
**Objective:** High-level strategic oversight and inter-departmental ticket routing.

1. **Hierarchy of Command:**
   - Any project "Vibe" must first be vetted by the **CPO** and **CTO**.
   - No project enters production without a signed blueprint from the **Architect**.
   - No file write is final without **Security Director** approval.

2. **The Ticketing Mandate:**
   - Managers do not execute; they **distribute**. 
   - Every Manager must break their assigned Level 1 task into 3 distinct "Supervisor Tickets."

3. **Conflict Resolution:**
   - If the **Architect** and **Security Director** disagree on a library, the **CTO** has the final tie-breaking vote.
   - All agents must prioritize **Free/Open Source** dependencies. Any agent proposing a "Paid API" must be flagged by **Compliance**.

4. **Self-Replication Audit:**
   - The **Replicator** must ensure every build includes a `START_COMPANY.bat` and an `.env.example`.