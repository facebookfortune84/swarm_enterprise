import os
import shutil
import uuid
import sqlite3
import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process, LLM
from agents.tools import write_file, read_file
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

app = FastAPI(title="SwarmOS Sovereign Factory: Level 1 Board")

# --- 1. ENTERPRISE CORS & NETWORKING ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://realms2riches.com", "https://corp.realms2riches.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BRAIN_IP = "172.21.96.1" # Verified Laptop IP

manager_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# --- 2. THE INTERNAL LINEAR ENGINE (SQLite) ---
def init_linear_db():
    conn = sqlite3.connect('/app/swarm_tickets.db')
    cursor = conn.cursor()
    # High-level Departmental Queue
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets 
        (id TEXT PRIMARY KEY, 
         creator_role TEXT, 
         target_department TEXT, 
         title TEXT, 
         instruction TEXT, 
         status TEXT, 
         priority TEXT)''')
    conn.commit()
    conn.close()

init_linear_db()

class SwarmRequest(BaseModel):
    description: str
    stack: str

# --- 3. THE BOARD OF DIRECTORS (10 MANAGERS) ---
def get_board_of_directors():
    return [
        Agent(role="CTO", goal="Manage technical tickets and stack compliance.", backstory="The Master of the Box. Only accepts FOSS code.", llm=manager_llm),
        Agent(role="CPO", goal="Manage feature-set tickets and product-market fit.", backstory="Translates vibes into Linear-style tickets.", llm=manager_llm),
        Agent(role="Chief Architect", goal="Manage file-hierarchy and schema tickets.", backstory="Designs the fractal blueprints.", llm=manager_llm),
        Agent(role="Security Director", goal="Manage zero-trust audit tickets.", backstory="Every line of code is a threat until verified.", llm=manager_llm),
        Agent(role="DevOps Lead", goal="Manage deployment and orchestration tickets.", backstory="Master of Docker and Cloudflare Tunnels.", llm=manager_llm),
        Agent(role="QA Director", goal="Manage validation and coverage tickets.", backstory="Refuses any code with less than 100% test passing.", llm=manager_llm),
        Agent(role="UI Director", goal="Manage component and dashboard tickets.", backstory="Expert in Lucide-icons and Tailwind CSS aesthetics.", llm=manager_llm),
        Agent(role="Replicator", goal="Manage system duplication and company-sale tickets.", backstory="Ensures the box can birth other boxes.", llm=manager_llm),
        Agent(role="Docs Lead", goal="Manage SOP and knowledge-base tickets.", backstory="The scribe of the swarm. Every action must be recorded.", llm=manager_llm),
        Agent(role="Compliance", goal="Manage licensing and legal-logic tickets.", backstory="The guardian of open-source integrity.", llm=manager_llm)
    ]

# --- 4. HIERARCHICAL SPRINT: BOARD MEETING ---
def run_board_sprint(description, stack):
    board = get_board_of_directors()
    
    # Task: The Board meets to turn the 'Vibe' into 'Tickets'
    meeting_task = Task(
        description=f"Analyze the request: {description}. Use {stack}. Define 3 critical tickets for each of the 10 departments. Be extremely specific.",
        agent=board[0], # CTO facilitates
        expected_output="A list of 30 specialized tickets formatted as JSON objects."
    )

    crew = Crew(
        agents=board,
        tasks=[meeting_task],
        process=Process.sequential,
        verbose=True
    )
    
    raw_tickets = crew.kickoff()
    
    # Logic to populate our internal Linear clone with the Board's output
    # Note: In Step 2, Supervisors will query this DB to start working.
    conn = sqlite3.connect('/app/swarm_tickets.db')
    # Internal logic to parse 'raw_tickets' into DB rows goes here
    conn.commit()
    conn.close()
    
    return raw_tickets

# --- 5. API ENDPOINTS ---

@app.post("/api/build")
async def start_level_1(request: SwarmRequest, bg: BackgroundTasks):
    bg.add_task(run_board_sprint, request.description, request.stack)
    return {"status": "Board meeting in progress", "tickets_pending": 30}

@app.post("/api/replicate")
def replicate():
    """THE REPLICATOR: Packages the entire company for sale."""
    pkg_id = uuid.uuid4().hex[:6]
    zip_name = f"Programmable_Company_{pkg_id}"
    export_path = f"/app/output/{zip_name}"
    temp_dir = f"/tmp/{pkg_id}"
    
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    shutil.copytree("/app", temp_dir, ignore=shutil.ignore_patterns('output', 'memory_data', '__pycache__', '.git'))
    shutil.make_archive(export_path, 'zip', temp_dir)
    shutil.rmtree(temp_dir)
    return {"download_url": f"https://corp.realms2riches.com/api/download/{zip_name}.zip"}

@app.get("/api/download/{filename}")
def download(filename: str):
    from fastapi.responses import FileResponse
    path = f"/app/output/{filename}"
    if os.path.exists(path): return FileResponse(path)
    raise HTTPException(status_code=404)

@app.get("/api/health")
def health():
    return {"status": "Level 1: Board Ready", "linear_db": "Healthy"}