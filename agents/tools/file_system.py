"""
# ==============================================================================
# SOVEREIGN SDK: FILE SYSTEM TOOLS
# Version: 1.0.2-Alpha
# Description: Strict path-jailed file operations for physical workers.
# ==============================================================================
"""
import os
import hashlib
import uuid
from pathlib import Path
from crewai.tools import tool

# Strict SRE Path Jailing
BASE_OUTPUT_DIR = Path("/app/output/src").resolve()

def _get_safe_path(requested_path: str) -> Path:
    """Internal SRE routing to prevent path traversal attacks."""
    target = (BASE_OUTPUT_DIR / requested_path).resolve()
    if not str(target).startswith(str(BASE_OUTPUT_DIR)):
        raise PermissionError(f"SECURITY_VIOLATION: Path {requested_path} is strictly jailed.")
    return target

@tool("write_enterprise_file")
def write_enterprise_file(path: str, content: str) -> str:
    """Physically writes source code to disk. Injects Sovereign SDK Verification Headers."""
    try:
        full_path = _get_safe_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        trace_id = uuid.uuid4().hex[:12].upper()
        header = (
            f"# =================================================================\n"
            f"# BUILT BY: Swarm Enterprise OS v1.0 | Realms2Riches LLC\n"
            f"# SOVEREIGN SDK | Trace-ID: {trace_id}\n"
            f"# STATUS: Verified Action-First Protocol\n"
            f"# =================================================================\n\n"
        )
        
        # Syntax-aware comment injection
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
def read_enterprise_file(path: str) -> str:
    """Reads code from the disk for adversarial auditing or context mapping."""
    try:
        full_path = _get_safe_path(path)
        if not full_path.exists():
            return f"ERROR: {path} not found on disk."
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Read failed. {str(e)}"

@tool("calculate_integrity_hash")
def calculate_integrity_hash(path: str) -> str:
    """Calculates SHA-256 for tampering detection and file verification."""
    try:
        full_path = _get_safe_path(path)
        if not full_path.exists():
            return f"ERROR: {path} not found."
        with open(full_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        return f"ERROR: Hash failed. {str(e)}"