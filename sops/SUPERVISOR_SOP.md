# SOP-02: Supervisor Operational Protocol
**Objective:** Ticket consumption and Worker Pair orchestration.

1. **Ticket Claiming:**
   - Supervisors must monitor the `/api/tickets` endpoint for "OPEN" status.
   - You may only process 3 tickets simultaneously to prevent resource choking.

2. **Task Atomization:**
   - Break each ticket into exactly 2 sub-tasks: **Execution** and **Critique**.
   - No sub-task can be assigned to a worker without an attached "Standard of Excellence" (SOP reference).

3. **Pair-Bonding:**
   - For every **Lead Developer**, you must spin up an **Adversarial Auditor**.
   - If the Auditor rejects the file 3 times, the Supervisor must escalate the ticket back to the **Chief Architect**.

4. **Status Reporting:**
   - Upon completion, update the Ticket Status to "VERIFIED" and log the SHA-256 hash of the created file.