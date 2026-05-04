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
    Monitors the Linear Engine and dispatches agents in a fractal hierarchy.
    Enforces SOP-02.6 (RAM Protection) and SOP-08 (Self-Healing).
    """

    def __init__(self):
        self.is_running = False
        self.polling_interval = 10 
        # Semaphore: Protects the 30GB Laptop RAM from concurrent 70B model calls
        self.execution_semaphore = threading.Semaphore(3)

    def start_production_loop(self) -> NoReturn:
        """Daemon entry point. Drives the factory from Strategy to Action."""
        self.is_running = True
        logger.info("ORCHESTRATOR: Production Loop Active. Monitoring for Tickets...")

        while self.is_running:
            try:
                self._dispatch_hierarchy()
                time.sleep(self.polling_interval)
            except Exception as e:
                logger.error(f"ORCHESTRATOR_CRITICAL: {e}")
                time.sleep(20) # Auto-recovery cooldown

    def _dispatch_hierarchy(self):
        """Routes tickets based on their level in the Fractal Tree."""
        session = swarm_db.Session()
        
        # --- LEVEL 1: THE BOARD (Strategic Directives) ---
        root_tickets = session.query(Ticket).filter(
            Ticket.creator_role == "USER",
            Ticket.status == TicketStatus.OPEN
        ).all()

        for rt in root_tickets:
            logger.info(f"ORCHESTRATOR: Root Directive {rt.id} found. Convening Board...")
            threading.Thread(target=self._run_board_meeting, args=(rt,)).start()
            swarm_db.claim_ticket(rt.id, "BOARD_OF_DIRECTORS")

        # --- LEVEL 2: THE SUPERVISORS (Departmental Execution) ---
        open_directives = session.query(Ticket).filter(
            Ticket.assigned_role.like("%Supervisor"),
            Ticket.status == TicketStatus.OPEN
        ).all()

        for ticket in open_directives:
            if self.execution_semaphore.acquire(blocking=False):
                logger.info(f"ORCHESTRATOR: Dispatching {ticket.assigned_role} for {ticket.id}")
                threading.Thread(target=self._managed_supervisor_run, args=(ticket.id,)).start()
            else:
                logger.debug("ORCHESTRATOR_WAIT: Concurrency limit reached.")

        session.close()

    def _run_board_meeting(self, ticket: Ticket):
        """Triggers the 12-Manager strategic session via Groq 70B."""
        try:
            strategic_board.convene_board(
                project_id=ticket.project_id,
                name=ticket.title,
                description=ticket.instruction,
                stack="Enterprise Fractal Stack"
            )
            swarm_db.update_ticket(ticket.id, status=TicketStatus.COMPLETED)
        except Exception as e:
            logger.error(f"BOARD_FAIL: {e}")
            swarm_db.update_ticket(ticket.id, status=TicketStatus.REJECTED)

    def _managed_supervisor_run(self, ticket_id: str):
        """Executes a supervisor task within the RAM-protection semaphore."""
        try:
            supervisor_orchestrator.process_ticket(ticket_id)
        finally:
            self.execution_semaphore.release()

    def stop(self):
        self.is_running = False
        logger.info("ORCHESTRATOR: Shutting down.")

main_orchestrator = SwarmOrchestrator()