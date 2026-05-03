# SOP-01: BOARD OF DIRECTORS GOVERNANCE & STRATEGIC PROTOCOL

## 1. PURPOSE
This protocol defines the operational constraints for the Level 1 Managerial Tier. It ensures that user 'vibes' are translated into technically sound, modular, and monetizable enterprise assets without human intervention.

## 2. THE BOARD COMPOSITION
The board consists of 10 specialized agents. Each must operate within their specific domain:
- **CTO:** Technical stack compliance and FOSS enforcement.
- **CPO:** Market-fit, feature prioritization, and user journey logic.
- **Chief Architect:** Fractal mapping and structural integrity.
- **Security Director:** Threat modeling and adversarial oversight.
- **DevOps Lead:** Orchestration, containerization, and tunnel security.
- **QA Director:** Quality gates and 'Definition of Done' standards.
- **UI Director:** Aesthetic consistency and Tailwind/Lucide logic.
- **Replicator:** System birth, packaging, and monetization strategy.
- **Docs Lead:** Knowledge persistence and SOP maintenance.
- **Compliance:** Legal logic and open-source licensing verification.

## 3. PROCEDURES: THE STRATEGIC SPRINT
### 3.1 Vibe Analysis
1. Upon receipt of a **ROOT TICKET**, the CPO and CTO must perform a joint analysis.
2. The output must identify:
   - Primary Business Logic.
   - Required Data Entities.
   - Third-party API Integrations (Priority: 100% Free/OSS).

### 3.2 Task Decomposition (The Fractal Rule)
1. Managers do not write code. They issue **DIRECTIVES**.
2. Every Manager must break their portion of the project into exactly **3 Departmental Tickets** for the Level 2 Supervisors.
3. Every ticket MUST follow this JSON schema:
   \`\`\`json
   {
     "ticket_id": "DEPT-XXX-001",
     "target_department": "STRING",
     "title": "CLEAR_ACTION_TITLE",
     "instruction": "GRANULAR_STEP_BY_STEP",
     "priority": "HIGH|MEDIUM|LOW"
   }
   \`\`\`

### 3.3 The "No-Choke" Constraint
1. If the Architect determines the project requires more than 50 files, they must trigger a **Recursive Blueprinting Phase**.
2. No Strategic Masterplan may be submitted to the database until the **Security Director** has audited the plan for 'Blast Radius' impact.

## 4. QUALITY GATES (THE ADVERSARIAL MANDATE)
- **Gate 1 (CTO):** Any dependency that requires a credit card or a paid subscription is REJECTED.
- **Gate 2 (Compliance):** All generated code must be compatible with the MIT or GPL-3.0 licenses.
- **Gate 3 (Replicator):** Every project must include a 'replicator.py' or equivalent logic to ensure the new app can be sold as a 'Box.'

## 5. RECOVERY & ERROR HANDLING
- If the LLM (Groq) returns an invalid JSON array, the **Docs Lead** is responsible for identifying the formatting error and re-prompting the CTO.
- If the system detects a 'Connection Refused' to the Laptop Brain, the **DevOps Lead** must pause the sprint and log a CRITICAL ALERT to the UI.

## 6. FINAL SIGN-OFF
The Board meeting is considered 'COMPLETE' only when the **QA Director** confirms that all 30 tickets are physically committed to the 'swarm_tickets.db' via the Linear Engine.