# SOP-09: AUTOMATED MARKETING & OUTREACH PROTOCOL

## 1. PURPOSE
This protocol governs the **Marketing Director** (Level 1) and the **Outreach Supervisor** (Level 2). It defines how the swarm identifies potential buyers and initiates sales sequences for the generated "Boxes."

## 2. THE CONTENT LOOP
1. **Content Creator Agent:** Uses the 'read_enterprise_file' tool to analyze the latest build in /output/src/.
2. **Action:** Generates a technical 1-page "Sales Spec" highlighting the FOSS nature and scalability of the specific build.

## 3. THE OUTREACH HANDSHAKE
1. **Lead Scraper Agent:** (Future Module) Identifies potential users on GitHub/LinkedIn.
2. **Outreach Manager Agent:** Uses the 'send_outreach_email' tool to deliver the Sales Spec.
3. **Verification:** All outreach must be logged in the 'swarm_tickets.db' with a status of 'OUTREACH_SENT'.

## 4. COMPLIANCE & OPT-OUT
- Every email MUST include an unsubscribe link pointing to 'https://realms2riches.com/api/auth/opt-out'.
- If the 'OUTREACH_ENABLED' flag in .env is 'false', this entire department must remain in 'STASIS' mode.