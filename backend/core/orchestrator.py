import time
import logging
import threading
from typing import NoReturn
from backend.db.linear_engine import swarm_db
from backend.db.models import TicketStatus, Ticket
from agents.supervisors.dept_leads import supervisor_orchestrator
from agents.managers.board import strategic_board

logger = logging.getLogger("SwarmOrchestrator")

class SwarmOrchestrator:
    """
    The Central Control Loop for Swarm Enterprise.
    Monitors the Linear Engine (SQLite) and dispatches agents based 
    on ticket priority and hierarchical level.
    Follows SOP-08 (Site Reliability & Self-Sustenance).
    """

    def __init__(self):
        self.is_running = False
        self.polling_interval = 10 # Seconds between database scans
        self.max_concurrent_tasks = 3 # SOP-02.6: Protect Laptop RAM

    def start_production_loop(self) -> NoReturn:
        """
        Main entry point for the background daemon.
        This loop runs forever, driving the fractal swarm.
        """
        self.is_running = True
        logger.info("ORCHESTRATOR: Production Loop Active. Monitoring Linear Engine...")

        while self.is_running:
            try:
                self._process_open_tickets()
                time.sleep(self.polling_interval)
            except Exception as e:
                logger.error(f"ORCHESTRATOR_CRITICAL: Loop encountered error: {e}")
                time.sleep(30) # Cool down before self-healing

    def _process_open_tickets(self):
        """
        Queries the DB for tickets that need agent intervention.
        Routes them to Level 1 (Board) or Level 2 (Supervisors).
        """
        session = swarm_db.Session()
        
        # 1. Check for Level 1 (Board) Strategic Planning Needs
        # These are tickets created by the API 'build' endpoint
        root_tickets = session.query(Ticket).filter(
            Ticket.creator_role == "USER",
            Ticket.status == TicketStatus.OPEN
        ).all()

        for rt in root_tickets:
            logger.info(f"ORCHESTRATOR: Root Ticket detected: {rt.id}. Convening Board...")
            # We run the board meeting in a separate thread to keep the loop moving
            threading.Thread(
                target=self._run_board_meeting, 
                args=(rt.project_id, rt.title, rt.instruction)
            ).start()
            # Mark as claimed immediately so it doesn't double-trigger
            swarm_db.claim_ticket(rt.id, "BOARD_OF_DIRECTORS")

        # 2. Check for Level 2 (Supervisor) Execution Needs
        # These are tickets created by the Board for specific departments
        dept_tickets = session.query(Ticket).filter(
            Ticket.assigned_role.like("%Supervisor"),
            Ticket.status == TicketStatus.OPEN
        ).limit(self.max_concurrent_tasks).all()

        for dt in dept_tickets:
            logger.info(f"ORCHESTRATOR: Dispatching {dt.assigned_role} for Ticket {dt.id}")
            # Sequential execution per Supervisor to prevent local LLM choking
            threading.Thread(
                target=supervisor_orchestrator.process_ticket,
                args=(dt.id,)
            ).start()

        session.close()

    def _run_board_meeting(self, project_id: str, name: str, description: str):
        """Wrapper to trigger the Level 1 strategic meeting."""
        try:
            # strategic_board was imported from File #7
            strategic_board.convene_board(
                project_id=project_id,
                name=name,
                description=description,
                stack="Standardized Fractal Stack" # Can be dynamic
            )
        except Exception as e:
            logger.error(f"ORCHESTRATOR_ERROR: Board meeting failed for {project_id}: {e}")

    def stop(self):
        """Graceful shutdown for system maintenance."""
        self.is_running = False
        logger.info("ORCHESTRATOR: Shutting down production loop...")

# Singleton instance to be used by the FastAPI lifecycle
main_orchestrator = SwarmOrchestrator()