import os
import json
import re
import logging
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
from agents.llm_config import MANAGER_BRAIN, EMBEDDER_CONFIG
from backend.db.linear_engine import swarm_db

logger = logging.getLogger("SwarmBoard")

class SwarmBoard:
    """
    Level 1: The Strategic Tier.
    Coordinates 12 specialized managers to translate high-level business 
    vision into technical departmental directives (Tickets).
    Follows SOP-01 (Board Governance) and SOP-09 (Marketing/Outreach).
    """

    def __init__(self):
        self.brain = MANAGER_BRAIN
        self.embedder = EMBEDDER_CONFIG

    def _get_manager_agents(self) -> List[Agent]:
        """Defines the 12 distinct seats on the Board of Directors."""
        return [
            Agent(
                role="CTO (Chief Technology Officer)",
                goal="Ensure 100% open-source compliance and high-scale technical scalability.",
                backstory="The final authority on the tech stack. You veto any proprietary or paid dependencies.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="CPO (Chief Product Officer)",
                goal="Translate the vision into a competitive, high-value feature set.",
                backstory="Master of user journeys. You define the core business logic of the target app.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Chief Architect",
                goal="Design the fractal folder structure and global data schemas.",
                backstory="Master of modularity. You map the system before any code is written.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Security Director",
                goal="Enforce zero-trust architecture and adversarial audit protocols.",
                backstory="Expert at threat modeling. You set the Risk SOP for all sub-tiers.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="DevOps Director",
                goal="Manage the containerization, orchestration, and self-healing strategy.",
                backstory="Infrastructure wizard. You ensure the app is a portable 'Box'.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="QA Director",
                goal="Define the 'Definition of Done' and logic verification standards.",
                backstory="Accuracy obsessed. You ensure every ticket has an audit step.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="UI/UX Director",
                goal="Design the enterprise aesthetic and frontend component logic.",
                backstory="Specialist in Tailwind/Lucide systems and dark-mode dashboards.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Marketing Director",
                goal="Architect the value proposition and automated sales positioning.",
                backstory="Expert in SaaS growth hacking. You define the 'Sales Spec' requirements for the build.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Outreach Director",
                goal="Design the automated lead generation and SMTP communication sequences.",
                backstory="Master of cold outreach and CRM logic. You ensure the company finds its buyers.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Replicator Lead",
                goal="Ensure the system can replicate its own file system and monetization logic.",
                backstory="Expert in digital asset delivery. You focus on the 'Box' resale value.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Documentation Manager",
                goal="Create granular SOPs for the Supervisors and Workers to follow.",
                backstory="Scribe of the Swarm. You ensure no logic is undocumented.",
                llm=self.brain, verbose=True
            ),
            Agent(
                role="Compliance Manager",
                goal="Monitor legal logic, licensing, and data privacy protocols.",
                backstory="Guardian of FOSS integrity and regulatory compliance.",
                llm=self.brain, verbose=True
            )
        ]

    def _parse_directives(self, output: str) -> List[Dict[str, Any]]:
        """Extracts JSON tickets from the board meeting results using regex."""
        try:
            # Look for the JSON block in the LLM output
            match = re.search(r'\[\s*\{.*\}\s*\]', output, re.DOTALL)
            if match:
                return json.loads(match.group())
            logger.error("PARSER_FAIL: No valid JSON array found in Board output.")
            return []
        except Exception as e:
            logger.error(f"PARSER_CRITICAL: JSON decoding error: {e}")
            return []

    def convene_board(self, project_id: str, name: str, description: str, stack: str):
        """
        Runs the Level 1 strategic meeting. 
        Decomposes the Project Vibe into 36 Departmental Tickets.
        """
        agents = self._get_manager_agents()
        
        meeting_task = Task(
            description=(
                f"PROJECT_ID: {project_id}\n"
                f"PROJECT_NAME: {name}\n"
                f"DESCRIPTION: {description}\n"
                f"TECH_STACK: {stack}\n\n"
                "CONSTITUTIONAL MANDATE:\n"
                "1. Each of the 12 Managers must provide 3 specialized technical tickets.\n"
                "2. Tickets must be atomic, technical, and actionable by Level 2 Supervisors.\n"
                "3. Marketing and Outreach must define the sales funnel and email templates.\n"
                "4. FORMAT: You MUST return a JSON array of objects with keys: "
                "['ticket_id', 'target_department', 'title', 'instruction', 'priority'].\n"
                "5. All instructions must be 100% complete. NO PLACEHOLDERS."
            ),
            agent=agents[0], # CTO Facilitates
            expected_output="A Strategic Masterplan containing exactly 36 technical JSON tickets."
        )

        board_crew = Crew(
            agents=agents,
            tasks=[meeting_task],
            process=Process.sequential, 
            embedder=self.embedder,
            verbose=True
        )

        logger.info(f"BOARD_MEETING: Starting strategic decomposition for {project_id}")
        raw_result = str(board_crew.kickoff())
        
        directives = self._parse_directives(raw_result)
        
        if not directives:
            raise ValueError("Board failed to generate a valid Masterplan.")

        # Persist directives to the Linear Engine for Level 2 processing
        for d in directives:
            swarm_db.create_ticket(
                project_id=project_id,
                title=d.get('title', 'Unknown Task'),
                instruction=d.get('instruction', ''),
                creator_role=d.get('target_department', 'CTO'),
                assigned_role=f"{d.get('target_department')} Supervisor", 
                priority=d.get('priority', 'MEDIUM')
            )
            
        logger.info(f"BOARD_COMPLETE: 36 directives committed to database for {project_id}")
        return directives

# Singleton instance
strategic_board = SwarmBoard()