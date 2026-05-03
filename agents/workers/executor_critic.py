import re
import logging
from typing import Dict, Any, Optional
from crewai import Agent, Task, Crew, Process
from agents.tools import write_enterprise_file, read_enterprise_file, calculate_integrity_hash, map_project_structure
from agents.llm_config import WORKER_BRAIN, EMBEDDER_CONFIG
from backend.db.linear_engine import swarm_db

logger = logging.getLogger("WorkerPair")

class AdversarialWorkerPair:
    """
    Level 3: The Execution Tier.
    Implements a high-precision, two-agent protocol for physical file generation.
    Enforces the 'Adversarial Mandate' where no code is trusted until verified.
    """

    def __init__(self):
        # Tools provided for physical disk manipulation
        self.tools = [
            write_enterprise_file, 
            read_enterprise_file, 
            calculate_integrity_hash,
            map_project_structure
        ]
        self.brain = WORKER_BRAIN

    def _extract_sha256(self, text: str) -> Optional[str]:
        """Regex helper to find the cryptographic hash in agent responses."""
        match = re.search(r'([a-fA-F0-9]{64})', text)
        return match.group(1) if match else None

    def process_ticket(self, ticket_id: str, file_path: str, instruction: str) -> Dict[str, Any]:
        """
        Executes a single technical ticket.
        Workflow: Lead Developer writes -> Security Overseer audits -> DB Updates.
        """
        logger.info(f"WORKER_START: Processing {ticket_id} for path {file_path}")

        # 1. THE EXECUTOR (SOP-03: Action-Only)
        executor = Agent(
            role="Senior Lead Developer",
            goal=f"Physically write the production-grade code for {file_path}",
            backstory=(
                "You are an Action-Only terminal worker. You do not explain code. "
                "You follow SOP-03 strictly. You MUST use the write_enterprise_file tool. "
                "You provide the full, completed file content. Placeholders are a firing offense."
            ),
            tools=self.tools,
            llm=self.brain,
            allow_delegation=False,
            verbose=True
        )

        # 2. THE CRITIC (SOP-04: Adversarial Audit)
        critic = Agent(
            role="Security & Quality Overseer",
            goal=f"Audit the code in {file_path} and verify its SHA-256 integrity.",
            backstory=(
                "You are a hostile auditor who follows SOP-04. You treat all developer output "
                "as adversarial. You do not trust claims; you verify via read_enterprise_file. "
                "You classify risk from Very Low to High. You REJECT any code with security flaws."
            ),
            tools=self.tools,
            llm=self.brain,
            allow_delegation=False,
            verbose=True
        )

        # 3. TASK DEFINITIONS
        writing_task = Task(
            description=(
                f"TICKET: {ticket_id}\n"
                f"TARGET_PATH: {file_path}\n"
                f"LOGIC: {instruction}\n"
                "INSTRUCTION: Use the write_enterprise_file tool to save the code. "
                "Include the SHA-256 hash returned by the tool in your final answer."
            ),
            agent=executor,
            expected_output=f"Success message for {file_path} with SHA-256 hash."
        )

        audit_task = Task(
            description=(
                f"Verify {file_path}. Use read_enterprise_file. Perform a Risk Assessment. "
                "If logic is flawed or secrets are hardcoded, issue a REJECTION. "
                "If perfect, provide a Pass Report with the verified SHA-256 hash."
            ),
            agent=critic,
            context=[writing_task],
            expected_output="Final Audit Report with Pass/Fail status and Risk Level."
        )

        # 4. CREW EXECUTION
        crew = Crew(
            agents=[executor, critic],
            tasks=[writing_task, audit_task],
            process=Process.sequential,
            embedder=EMBEDDER_CONFIG,
            verbose=True
        )

        result = str(crew.kickoff())

        # 5. POST-EXECUTION DATABASE SYNC
        # Parse the final result to update the Linear Engine
        final_hash = self._extract_sha256(result)
        risk_match = re.search(r'Risk Level:\s*(VERY_LOW|LOW|MEDIUM|MEDIUM_HIGH|HIGH)', result, re.I)
        risk_level = risk_match.group(1).lower() if risk_match else "medium"
        
        status_action = "APPROVED" if "PASS" in result.upper() else "REJECTED"

        swarm_db.submit_work(ticket_id, file_path, result) # Log the content
        swarm_db.log_audit(
            ticket_id=ticket_id,
            auditor_role="Security_Overseer",
            risk=risk_level,
            action=status_action,
            findings=result
        )

        return {
            "ticket_id": ticket_id,
            "hash": final_hash,
            "status": status_action,
            "risk": risk_level
        }

# Singleton instance for the factory
execution_unit = AdversarialWorkerPair()