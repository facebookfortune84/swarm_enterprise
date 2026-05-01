from crewai.tools import tool
import os

@tool("write_file")
def write_file(path: str, content: str) -> str:
    """Physically writes code to /app/output/src/"""
    filename = os.path.basename(path)
    base_folder = "/app/output/src"
    if not os.path.exists(base_folder): os.makedirs(base_folder, exist_ok=True)
    full_path = os.path.join(base_folder, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"SUCCESS: Wrote {filename} to disk."

@tool("read_file")
def read_file(path: str) -> str:
    """Reads code from /app/output/src/"""
    filename = os.path.basename(path)
    full_path = os.path.join("/app/output/src", filename)
    if not os.path.exists(full_path): return "Error: File not found."
    with open(full_path, "r", encoding="utf-8") as f: return f.read()