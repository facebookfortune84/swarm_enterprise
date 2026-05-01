# SOP: Product Architecture & System Design
**Objective:** Translate high-level user "vibes" into a concrete, scalable technical blueprint.

1. **Requirements Decomposition:**
   - Define Every Actor: List all user roles (Admin, User, Guest).
   - Data Modeling: Create a Mermaid.js Entity Relationship Diagram (ERD).
   - Tech Stack Enforcement: If the user selects "React/Python," do not allow any deviations (e.g., no Next.js if they asked for pure React).

2. **The "Box" Compatibility Standard:**
   - All designs must be "Container-First." Every service must have a Health-Check endpoint.
   - Design for Multi-Tenancy: Assume the user will sell this app to multiple clients.

3. **File System Mapping:**
   - You must output a full directory tree BEFORE any code is written.
   - Standard structure: `/src` for code, `/tests` for QA, `/docs` for SOPs, `/deploy` for Docker.

4. **Scalability Constraints:**
   - Architecture must support horizontal scaling (stateless APIs).
   - Use Redis for caching and Celery/RabbitMQ for long-running tasks.