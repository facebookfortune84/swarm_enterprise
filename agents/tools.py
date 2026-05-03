import os
import hashlib
import shutil
import uuid
from pathlib import Path
from typing import List, Optional
from crewai.tools import tool

# --- CONFIGURATION ---
# The Jailed Root: All agent actions are physically locked to this directory
BASE_OUTPUT_DIR = Path("/app/output/src")

class SwarmTools:
    """
    Hardened File System Tools with Sovereign Trace Protocol.
    Implements cryptographic verification, path jailing, and SDK header injection.
    """

    @staticmethod
    def _get_safe_path(requested_path: str) -> Path:
        """Enforces Path Jailing to prevent directory traversal attacks."""
        base = BASE_OUTPUT_DIR.resolve()
        target = (base / requested_path).resolve()
        
        if not str(target).startswith(str(base)):
            raise PermissionError(f"SECURITY_VIOLATION: Attempt to access {requested_path} blocked.")
        return target

    @tool("write_enterprise_file")
    def write_file(path: str, content: str) -> str:
        """
        Physically writes source code to the disk with Sovereign SDK Headers.
        Mandatory for the Lead Developer (SOP-03).
        Input: relative path (e.g., 'api/main.py') and full file content.
        Returns: Success message and SHA-256 hash.
        """
        try:
            full_path = SwarmTools._get_safe_path(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # MAGNIFICENT UPDATE: Generate Sovereign SDK Header
            # This 'birthmark' proves the code was built by your autonomous factory.
            trace_id = uuid.uuid4().hex[:12].upper()
            header = (
                f"# =================================================================\n"
                f"# BUILT BY: Swarm Enterprise OS v1.0 | Realms2Riches LLC\n"
                f"# SOVEREIGN SDK | Trace-ID: {trace_id}\n"
                f"# STATUS: Verified Action-First Protocol\n"
                f"# =================================================================\n\n"
            )
            
            # For non-python files, we adjust comment style slightly in a robust way
            if path.endswith(('.js', '.css', '.ts')):
                header = header.replace('#', '//')
            elif path.endswith(('.html', '.xml')):
                header = f"<!-- \n{header.replace('#', '')}-->\n\n"

            final_content = header + content
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            
            # Calculate hash of the FINAL content for the Linear Engine Audit Log
            file_hash = hashlib.sha256(final_content.encode()).hexdigest()
            return f"SUCCESS: File {path} physically written. Trace: {trace_id} | SHA256: {file_hash}"
            
        except Exception as e:
            return f"ERROR: Write operation failed. {str(e)}"

    @tool("read_enterprise_file")
    def read_file(path: str) -> str:
        """
        Reads code from the disk for adversarial auditing.
        Mandatory for the Security & Quality Overseer (SOP-04).
        """
        try:
            full_path = SwarmTools._get_safe_path(path)
            if not full_path.exists():
                return f"ERROR: File {path} not found."
            
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"ERROR: Read operation failed. {str(e)}"

    @tool("map_project_structure")
    def map_structure(directory: str = ".") -> str:
        """
        Recursively maps the project tree.
        Used by the Architect (SOP-05) to maintain fractal structural integrity.
        """
        try:
            root = SwarmTools._get_safe_path(directory)
            tree = ["Root: /app/output/src"]
            for path in sorted(root.rglob("*")):
                if "__pycache__" in path.name or ".git" in path.name:
                    continue
                depth = len(path.relative_to(root).parts)
                spacer = "  " * depth
                tree.append(f"{spacer} - {path.name}")
            return "\n".join(tree)
        except Exception as e:
            return f"ERROR: Mapping failed. {str(e)}"

    @tool("calculate_integrity_hash")
    def get_file_hash(path: str) -> str:
        """
        Calculates the SHA-256 hash of an existing file.
        Used by the SRE and Auditor to detect tampering (SOP-08).
        """
        try:
            full_path = SwarmTools._get_safe_path(path)
            with open(full_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            return f"ERROR: Integrity check failed. {str(e)}"

    @tool("search_enterprise_logic")
    def grep_code(query: str) -> str:
        """
        Searches all files for logic patterns to enable cross-file updates.
        """
        results = []
        try:
            # We search the jailed src directory specifically
            for path in BASE_OUTPUT_DIR.rglob("*"):
                if path.is_file() and not "__pycache__" in str(path):
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        if query in f.read():
                            results.append(str(path.relative_to(BASE_OUTPUT_DIR)))
            
            return f"Logic found in: {', '.join(results)}" if results else "Query not found."
        except Exception as e:
            return f"ERROR: Logic search failed. {str(e)}"

    @tool("delete_enterprise_file")
    def remove_file(path: str) -> str:
        """
        Removes a file. Used for refactoring or pruning redundant logic.
        """
        try:
            full_path = SwarmTools._get_safe_path(path)
            if full_path.is_file():
                os.remove(full_path)
                return f"SUCCESS: {path} deleted."
            return f"ERROR: {path} is not a valid file."
        except Exception as e:
            return f"ERROR: Deletion failed. {str(e)}"

# Instantiate for import
swarm_tools = SwarmTools()
write_enterprise_file = swarm_tools.write_file
read_enterprise_file = swarm_tools.read_file
map_project_structure = swarm_tools.map_structure
calculate_integrity_hash = swarm_tools.get_file_hash
search_enterprise_logic = swarm_tools.grep_code
delete_enterprise_file = swarm_tools.remove_file