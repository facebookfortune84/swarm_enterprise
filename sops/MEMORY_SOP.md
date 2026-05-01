# SOP-05: Collective Memory & RAG Protocol
**Objective:** Eliminate redundant errors and ensure cross-agent knowledge transfer.

1. **The "Journaling" Requirement:**
   - After every successful code fix, the Critic agent must write a "Post-Mortem" to the Vector DB.
   - Format: `[Context] -> [Error] -> [Resolution] -> [SOP Update Suggestion]`.

2. **The "Recall" Phase:**
   - Before the Developer starts a new task, they must query the Vector DB for "similar past challenges."
   - If a previous solution exists, it MUST be used as the base template.

3. **Knowledge Persistence:**
   - Memory must be categorized into: `Technical_Debt`, `Security_Patterns`, and `User_Preferences`.