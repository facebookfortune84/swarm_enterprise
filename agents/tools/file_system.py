import os
import hashlib
import uuid
from pathlib import Path
from crewai.tools import tool

BASE_OUTPUT_DIR = Path("/app/output/src")

class SwarmTools:
    @staticmethod
    def _get_safe_path(requested_path: str) -> Path:
        base = BASE_OUTPUT_DIR.resolve()
        target = (base / requested_path).resolve()
        if not str(target).startswith(str(base)):
            raise PermissionError(f"SECURITY_VIOLATION: Path {requested_path} is jailed.")
        return target

    @tool("write_enterprise_file")
    def write_file(path: str, content: str) -> str:
        """Physically writes source code with Sovereign SDK Headers."""
        try:
            full_path = SwarmTools._get_safe_path(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            trace_id = uuid.uuid4().hex[:12].upper()
            header = (
                f"# =================================================================\n"
                f"# BUILT BY: Swarm Enterprise OS v1.0 | Realms2Riches LLC\n"
                f"# SOVEREIGN SDK | Trace-ID: {trace_id}\n"
                f"# STATUS: Verified Action-First Protocol\n"
                f"# =================================================================\n\n"
            )
            
            if path.endswith(('.js', '.css', '.ts')):
                header = header.replace('#', '//')
            elif path.endswith(('.html', '.xml')):
                header = f"<!-- \n{header.replace('#', '')}-->\n\n"

            final_content = header + content
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            
            file_hash = hashlib.sha256(final_content.encode()).hexdigest()
            return f"SUCCESS: Wrote {path}. Trace: {trace_id} | SHA256: {file_hash}"
        except Exception as e:
            return f"ERROR: Write failed. {str(e)}"

    @tool("read_enterprise_file")
    def read_file(path: str) -> str:
        """Reads code from the disk for adversarial auditing."""
        try:
            full_path = SwarmTools._get_safe_path(path)
            if not full_path.exists(): return f"ERROR: {path} not found."
            with open(full_path, "r", encoding="utf-8") as f: return f.read()
        except Exception as e:
            return f"ERROR: Read failed. {str(e)}"

    @tool("calculate_integrity_hash")
    def get_file_hash(path: str) -> str:
        """Calculates SHA-256 for tampering detection."""
        try:
            full_path = SwarmTools._get_safe_path(path)
            with open(full_path, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            return f"ERROR: Hash failed. {str(e)}"

# Export individual tools for the agents
swarm_tools = SwarmTools()
write_enterprise_file = swarm_tools.write_file
read_enterprise_file = swarm_tools.read_file
calculate_integrity_hash = swarm_tools.get_file_hash