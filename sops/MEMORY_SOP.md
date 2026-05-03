# SOP-06: SEMANTIC MEMORY & TRIBAL KNOWLEDGE PROTOCOL

## 1. PURPOSE
This protocol defines the standards for long-term persistence and retrieval of engineering intelligence. It ensures that the swarm maintains a cumulative knowledge base, preventing the repetition of logic errors and allowing for recursive self-optimization.

## 2. THE DUAL-STORE ARCHITECTURE
Intelligence must be stored across two distinct layers to ensure maximum retrieval accuracy:
- **Semantic Layer (ChromaDB):** High-dimensional vector storage for code patterns, architectural styles, and "Vibe" interpretations. 
- **Relational Layer (SQLite):** Structured historical data including ticket status, SHA-256 hashes, and Auditor rejection logs.

## 3. PROCEDURES: THE JOURNALING REQUIREMENT
Agents are mandated to "Journal" their state after every major task completion or failure.

### 3.1 After-Action Reports (AAR)
1. Upon a ticket reaching "VERIFIED" status, the **Lead Developer** must generate a "Success Pattern" summary.
2. Format: \`[Pattern Name] -> [Logic Implemented] -> [Challenge Overcome] -> [Code Snippet ID]\`.
3. This is pushed to the Semantic Layer via the \`memory_engine.py\`.

### 3.2 Post-Mortem Documentation (The Failure Loop)
1. Every time the **Security & Quality Overseer** issues a "REJECTION," a failure entry is created.
2. The **Docs Lead** must parse the rejection report and store it in the "Lessons Learned" vector collection.
3. Metadata for failure entries must include: \`ErrorCode\`, \`RootCause\`, and \`RemediationSteps\`.

## 4. PROCEDURES: THE RECALL PHASE (PRE-TASK)
No agent may begin a "Medium" or "High" risk task without performing a "Recall Query."

1. **Context Search:** Before designing a file, the **Architect** must search memory for "similar architectural patterns" built in previous projects.
2. **Anti-Pattern Verification:** The **Lead Developer** must query the memory for "Common Rejections" related to the current stack (e.g., "FastAPI CORS issues" or "Stripe Webhook signature failures").
3. **Requirement:** If a past failure is detected, the agent MUST explicitly mention the remediation in their current reasoning path.

## 5. RECURSIVE SOP UPDATING
The **CTO** and **Documentation Manager** are responsible for "Constitutional Evolution."
1. Every 5 successful projects, the **CTO** must task a Supervisor with "SOP Optimization."
2. The Supervisor reads the 10 most common rejections from the database.
3. If a pattern of error is identified, the Supervisor MUST physically update the relevant \`.md\` file in \`/app/sops/\` to include a new constraint that prevents that error.

## 6. VECTOR DATA STANDARDS
To ensure the "Company in a Box" remains portable and free to operate:
- **Embedding Model:** All semantic math must use the \`nomic-embed-text:latest\` model running locally on the Laptop Brain.
- **Privacy:** Under no circumstances are memory vectors to be sent to a cloud-based provider.
- **Persistence:** The ChromaDB index must be saved to the \`/app/memory_data/\` volume to survive container restarts.

## 7. KNOWLEDGE CATEGORIES
Memory must be tagged with the following categories for granular retrieval:
- \`CORE_INFRA\`: Docker, Tunnels, and VM configurations.
- \`BUSINESS_LOGIC\`: Specific industry rules (e.g., Legal workflows).
- \`SECURITY_PATTERNS\`: Cryptographic methods and auth implementations.
- \`UI_COMPONENTS\`: Reusable React/Tailwind patterns.

## 8. COMPLETION CRITERIA
A project is not "CLOSED" until the **QA Director** verifies that the "Lessons Learned" for that build have been successfully vectorized and the total memory count in ChromaDB has incremented.