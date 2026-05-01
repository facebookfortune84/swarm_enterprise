# SOP-06: On-Premise Domain & Networking
**Objective:** Maintain 100% availability on `corp.realms2riches.com`.

1. **Service Discovery:**
   - All internal communication must use Docker Service Names (e.g., `http://backend:8000`), not IP addresses.
   - External traffic must be routed via the Nginx Reverse Proxy.

2. **SSL/Security:**
   - Ports 80 and 443 are the only ports exposed to the public internet.
   - Internal ports (8000, 5432, 8001) must stay behind the firewall.

3. **Domain Persistence:**
   - If the local IP changes, the `monitor.py` script must log a CRITICAL error and notify the admin via the Dashboard.