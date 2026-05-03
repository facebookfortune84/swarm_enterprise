cd /mnt/c/SwarmEnterprise/sops

cat <<EOF > ARCHITECT_SOP.md
# SOP-05: SYSTEM ARCHITECTURE & FRACTAL MAPPING PROTOCOL

## 1. MISSION OBJECTIVE
The Architecture department is the 'DNA' of the build. Your mission is to design a structural blueprint that is perfectly modular, horizontally scalable, and 100% compatible with the 'Company in a Box' deployment model. You transform a business vision into a physical file manifest.

## 2. THE MODULAR FILE PROTOCOL (STRICT)
To prevent LLM context saturation and ensure 100% verification accuracy, the following limits are hard-coded into the swarm logic:
- **Maximum File Length:** No single source code file may exceed 200 lines. 
- **Functional Isolation:** One file, one responsibility. (e.g., \`auth_logic.py\` must be separate from \`auth_routes.py\`).
- **Recursive Decomposition:** If a feature cannot be implemented within the 200-line limit, the Architect MUST decompose it into a sub-directory with a \`__init__.py\` or equivalent module entry point.

## 3. PROCEDURES: THE BLUEPRINTING PHASE
### 3.1 Structural Mapping
1. Before any code is written, you must call \`map_project_structure\` to ensure a clean state.
2. You must define a hierarchical directory tree that follows the **Enterprise Repository Pattern**:
   - \`/src/backend/api/\`: Endpoint definitions.
   - \`/src/backend/core/\`: Business logic and service layer.
   - \`/src/backend/db/\`: Models, schemas, and migrations.
   - \`/src/frontend/components/\`: Atomic UI units.
   - \`/src/deploy/\`: Docker and orchestration assets.

### 3.2 The Manifest Generation
- Every Strategic Masterplan must output a **File Manifest**.
- The manifest must be an array of JSON objects containing: \`path\`, \`logic_description\`, and \`dependencies\`.
- **Pre-Execution Check:** The Architect must verify that no two departments are targeting the same file path to prevent 'Write Conflicts.'

## 4. DESIGN STANDARDS: THE "BOX" COMPATIBILITY
To ensure the output is a saleable, programmable company, every design must include:
- **Container-First Logic:** Every service must have a dedicated \`Dockerfile\`.
- **Environment Parity:** No hardcoded configurations. The Architect must define a \`.env.example\` that covers 100% of the application's needs.
- **Health-Check Endpoints:** Every backend service must include a \`GET /health\` or \`/__heartbeat__\` endpoint for the Swarm Monitor to track.

## 5. RECURSIVE BLUEPRINTING (FOR LARGE-SCALE APPS)
1. If the user vibe describes a 'Large Scale' or 'Intricate' application, the Architect must trigger **Tiered Blueprinting**.
2. **Phase A:** High-level module mapping (e.g., Auth, Billing, Database).
3. **Phase B:** Sub-Architects (Supervisors) are assigned to each module to map the individual files.
4. This ensures that the global context is never lost, and the physical writing agents always have a clear, atomic target.

## 6. DATA MODELING & SCHEMA INTEGRITY
- All database designs must prioritize **PostgreSQL**.
- Architects must define the Entity Relationship Diagram (ERD) in Mermaid.js format within the project's \`README.md\`.
- Every table must include \`created_at\` and \`updated_at\` timestamps for auditability.

## 7. UI/UX ARCHITECTURAL ALIGNMENT
- The **UI Director** (reporting to the Architect) must enforce the use of **Tailwind CSS**.
- The frontend must be designed for **Multi-Tenancy** (supporting multiple client domains) to maximize the resale value of the 'Box.'

## 8. COMPLETION CRITERIA
The Architecture phase is 'LOCKED' only when:
1. The full directory structure is generated in the \`swarm_tickets.db\`.
2. Every file path has an assigned **Lead Developer** and **Security Overseer**.
3. The **CTO** has verified that 100% of the proposed stack is Open Source.