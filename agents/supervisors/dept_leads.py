import os
import json
import re
import logging
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
from agents.llm_config import MANAGER_BRAIN, EMBEDDER_CONFIG
from agents.workers.executor_critic import execution_unit
from backend.db.linear_engine import swarm_db
from backend.db.models import TicketStatus

logger = logging.getLogger("SupervisorTier")

class SupervisorFactory:
    """
    Level 2: The Supervisory Tier.
    Dynamically generates Department Leads who manage Worker Pairs.
    Enforces SOP-02 (Supervisor Operational Protocol).
    """

    def __init__(self):
        self.brain = MANAGER_BRAIN  # Uses Groq 70B for decomposition logic
        self.embedder = EMBEDDER_CONFIG

    def _get_supervisor_role(self, department: str) -> str:
        """Maps Board departments to specific Supervisor roles (3 per department)."""
        dept_map = {
            "CTO": "Backend Infrastructure Lead",
            "CPO": "Core Logic Lead",
            "ARCHITECT": "System Hierarchy Supervisor",
            "SECURITY": "Vulnerability Mitigation Lead",
            "DEVOPS": "Containerization Orchestrator",
            "QA": "Logic Verification Lead",
            "UI": "Tailwind Component Architect",
            "REPLICATOR": "Packaging & Saleability Lead",
            "DOCS": "SOP Implementation Lead",
            "COMPLIANCE": "FOSS Integrity Auditor"
        }
        return dept_map.get(department.upper(), f"{department} General Lead")

    def process_ticket(self, ticket_id: str):
        """
        The Supervisor Loop:
        1. Claims an OPEN ticket from the DB.
        2. Plans the specific file structure required.
        3. Spawns Worker Pairs (Level 3) sequentially.
        """
        # 1. Ticket Acquisition
        session = swarm_db.Session()
        from backend.db.models import Ticket
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            logger.error(f"SUPERVISOR_ERROR: Ticket {ticket_id} not found.")
            return

        role_name = self._get_supervisor_role(ticket.creator_role)
        logger.info(f"SUPERVISOR_ACTIVE: {role_name} claiming ticket {ticket_id}")
        
        swarm_db.claim_ticket(ticket_id, role_name)

        # 2. Setup Supervisor Agent (Groq 70B)
        supervisor_agent = Agent(
            role=role_name,
            goal=f"Decompose the directive '{ticket.title}' into atomic file-writing tasks.",
            backstory=(
                f"You are the {role_name}. You follow SOP-02 strictly. "
                "You translate high-level directives into a specific list of files to be written. "
                "You oversee the execution unit and ensure each file is audited by the Critic."
            ),
            llm=self.brain,
            verbose=True
        )

        # 3. Planning Task (High-Reasoning)
        plan_task = Task(
            description=(
                f"DIRECTIVE: {ticket.instruction}\n\n"
                "STEP 1: List exactly which files need to be created or modified for this ticket.\n"
                "STEP 2: For each file, provide a 2-sentence implementation guide.\n"
                "FORMAT: You MUST return a JSON list of objects: [{'path': '...', 'task': '...'}]"
            ),
            agent=supervisor_agent,
            expected_output="A JSON manifest of physical file tasks."
        )

        planning_crew = Crew(
            agents=[supervisor_agent],
            tasks=[plan_task],
            process=Process.sequential,
            embedder=self.embedder
        )

        raw_plan = str(planning_crew.kickoff())
        file_tasks = self._parse_file_tasks(raw_plan)

        if not file_tasks:
            logger.warning(f"SUPERVISOR_IDLE: No files identified for ticket {ticket_id}")
            swarm_db.update_ticket(ticket_id, status=TicketStatus.COMPLETED)
            return

        # 4. Sequential Worker Delegation (SOP-02.3: One file at a time)
        # This prevents context choking and ensures 100% audit accuracy.
        for file_task in file_tasks:
            path = file_task.get('path')
            instruction = file_task.get('task')
            
            logger.info(f"SUPERVISOR_DELEGATING: Handing {path} to Level 3 Worker Pair.")
            
            # This triggers File #6 (executor_critic.py)
            worker_result = execution_unit.process_ticket(
                ticket_id=ticket_id,
                file_path=path,
                instruction=instruction
            )

            if worker_result['status'] == "REJECTED":
                logger.error(f"SUPERVISOR_INTERVENTION: Worker Pair rejected {path}. Escalating.")
                # Logic for retry or escalation per SOP-02.4
                break 

        # 5. Completion
        swarm_db.update_ticket(ticket_id, status=TicketStatus.COMPLETED)
        logger.info(f"SUPERVISOR_COMPLETE: Ticket {ticket_id} finalized.")

    def _parse_file_tasks(self, output: str) -> List[Dict[str, str]]:
        """Extracts the file list from the Supervisor's planning output."""
        try:
            match = re.search(r'\[\s*\{.*\}\s*\]', output, re.DOTALL)
            if match:
                return json.loads(match.group())
            return []
        except Exception:
            return []

# Singleton Instance for the Factory
supervisor_orchestrator = SupervisorFactory()