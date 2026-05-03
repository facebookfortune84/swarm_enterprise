# SOP-07: ENTERPRISE NETWORKING & SOVEREIGN CONNECTIVITY PROTOCOL

## 1. PURPOSE
This protocol ensures 100% uptime and secure routing for the Swarm Enterprise infrastructure. It defines the standards for external ingress via Cloudflare and internal lateral communication between the Windows Server VM and the Laptop Inference Gateway.

## 2. THE TOPOLOGY HIERARCHY
The system operates on a three-tier network isolation model:
- **Tier 1 (Public Edge):** Cloudflare Zero Trust Edge. Handles SSL termination and domain resolution for realms2riches.com.
- **Tier 2 (Internal Service Mesh):** Docker 'swarm_network'. Facilitates service discovery between the Backend, Frontend, and Database containers.
- **Tier 3 (Inference Bridge):** The NAT-crossing pipe between the WSL2 environment and the physical Laptop IP for Ollama access.

## 3. PROCEDURES: CLOUDFLARE TUNNEL (INGRESS)
The **DevOps Lead** is responsible for maintaining the tunnel integrity.

### 3.1 Protocol Enforcement
- **HTTP2 Requirement:** Tunnels must be initialized with \`--protocol http2\` to ensure stability over Windows Server virtualized adapters. QUIC (UDP) is restricted due to potential packet loss in the Hyper-V switch.
- **Ingress Mapping:**
  - \`realms2riches.com\` -> \`http://frontend:80\`
  - \`corp.realms2riches.com\` -> \`http://backend:8000\`
  - \`viewer.realms2riches.com\` -> \`http://output_viewer:8080\`

### 3.2 Security Headers
Every response served via the tunnel must include:
- \`X-Frame-Options: DENY\` (Prevents Clickjacking)
- \`X-Content-Type-Options: nosniff\`
- \`Strict-Transport-Security: max-age=31536000\`

## 4. PROCEDURES: THE INFERENCE BRIDGE (THE BRAIN PIPE)
The **SRE** is responsible for verifying the link to the Laptop Brain.

### 4.1 Dynamic IP Discovery
1. Upon system boot, the \`boot_swarm.ps1\` script must identify the Laptop IP via the VM's default gateway.
2. The IP must be injected into the \`.env\` as \`OLLAMA_URL\`.
3. The Docker container must use the alias \`host.docker.internal\` with the \`host-gateway\` mapping to resolve this IP.

### 4.2 Firewall Handshake
- **Laptop Side:** Port 11434 must be open to the \`172.16.0.0/12\` subnet.
- **VM Side:** Outbound traffic on 11434 must be white-listed for the Docker process.

## 5. DOCKER SERVICE DISCOVERY
Agents are forbidden from using hardcoded IP addresses for internal communication.
- **Rule:** Use service names only.
  - Correct: \`http://chromadb:8000\`
  - Incorrect: \`http://172.18.0.5:8000\`
- **Isolation:** The Database and Memory containers must NOT expose ports to the Windows Host. They must only be reachable via the \`swarm_network\`.

## 6. CROSS-ORIGIN RESOURCE SHARING (CORS)
To prevent '403 Forbidden' or 'Blocked by CORS' errors in the Dashboard:
1. The Backend (FastAPI) must explicitly allow the origins defined in the \`MANAGER_SOP.md\`.
2. Credentials must be allowed (\`allow_credentials=True\`) to facilitate authenticated zipping and downloads.

## 7. SELF-HEALING NETWORK PROTOCOLS
If the **Monitor Agent** detects a network failure (Error 1033 or 502):
1. **Step 1:** Ping the internal service name (e.g., \`ping backend\`).
2. **Step 2:** If unreachable, restart the specific service container.
3. **Step 3:** If internal ping succeeds but external access fails, restart the \`tunnel\` container.
4. **Step 4:** Log the 'Root Cause' to the RAG memory for the Replicator to audit.

## 8. "COMPANY IN A BOX" PORTABILITY STANDARDS
To ensure the build is saleable, the networking must be "Universal":
- The \`docker-compose.yml\` must use relative volume paths (\`./output\`).
- The \`config.yml\` for the tunnel must be generated dynamically to support the buyer's unique domain name.

## 9. COMPLETION CRITERIA
The Network phase is marked 'HEALTHY' only when:
1. \`docker exec swarm-tunnel curl http://backend:8000/api/health\` returns 200 OK.
2. The Cloudflare Zero Trust Dashboard shows the 'Swarm-Production' connector as 'ACTIVE'.
3. The SHA-256 integrity of the \`docker-compose.yml\` matches the record in the Linear Engine.