"""
# ==============================================================================
# SOVEREIGN SDK: HEARTBEAT ORCHESTRATOR
# Version: 1.0.1-Alpha
# Description: The central hierarchy manager.
# ==============================================================================
"""
import time
import logging
import threading
from typing import NoReturn
from backend.db.linear_engine import swarm_db
from backend.db.models import TicketStatus, Ticket
from agents.supervisors.dept_leads import supervisor_orchestrator
from agents.managers.board import strategic_board

# Configure industrial logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("SwarmOrchestrator")

class SwarmOrchestrator:
    """
    Central Control Loop for Swarm Enterprise.
    Monitors the Linear Engine and dispatches agents in a fractal hierarchy.
    """

    def __init__(self):
        self.is_running = False
        self.polling_interval = 10 
        # Semaphore: Protects the 30GB Laptop RAM from concurrent Groq/Ollama context floods
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
                logger.error(f"ORCHESTRATOR_CRITICAL_RECOVERY: {e}")
                time.sleep(20) # Auto-recovery cooldown delay

    def _dispatch_hierarchy(self):
        """Routes tickets based on their level in the Fractal Tree."""
        session = swarm_db.Session()
        try:
            # --- LEVEL 1: THE BOARD (Strategic Directives) ---
            # USER tickets that are open move to L1 Management
            root_tickets = session.query(Ticket).filter(
                Ticket.creator_role == "USER",
                Ticket.status == TicketStatus.OPEN
            ).all()

            for rt in root_tickets:
                logger.info(f"ORCHESTRATOR: Root Directive {rt.id} detected. Convening Board...")
                # SRE PROTECTION: Pass extracted data, not the live object, to the thread
                args = (rt.id, rt.project_id, rt.title, rt.instruction)
                threading.Thread(target=self._run_board_meeting, args=args).start()
                swarm_db.claim_ticket(rt.id, "BOARD_OF_DIRECTORS")

            # --- LEVEL 2: THE SUPERVISORS (Tactical Dispatch) ---
            open_directives = session.query(Ticket).filter(
                Ticket.assigned_role.like("%Supervisor"),
                Ticket.status == TicketStatus.OPEN
            ).all()

            for ticket in open_directives:
                if self.execution_semaphore.acquire(blocking=False):
                    logger.info(f"ORCHESTRATOR: Handing Ticket {ticket.id} to {ticket.assigned_role}")
                    threading.Thread(target=self._managed_supervisor_run, args=(ticket.id,)).start()
                else:
                    logger.debug("ORCHESTRATOR_QUEUE_FULL: Concurrency threshold reached.")
        finally:
            session.close()

    def _run_board_meeting(self, t_id: str, p_id: str, title: str, instruction: str):
        """Triggers the 12-Manager strategic session via Groq."""
        try:
            strategic_board.convene_board(
                project_id=p_id,
                name=title,
                description=instruction,
                stack="Enterprise Fractal Stack"
            )
            swarm_db.update_ticket(t_id, status=TicketStatus.COMPLETED)
        except Exception as e:
            logger.error(f"ORCHESTRATOR_BOARD_FAILURE: {e}")
            swarm_db.update_ticket(t_id, status=TicketStatus.REJECTED)

    def _managed_supervisor_run(self, ticket_id: str):
        """Executes a supervisor task inside the RAM-protection gate."""
        try:
            supervisor_orchestrator.process_ticket(ticket_id)
        except Exception as e:
            logger.error(f"ORCHESTRATOR_SUPERVISOR_FAILURE for Ticket {ticket_id}: {e}")
        finally:
            self.execution_semaphore.release()

    def stop(self):
        """Shutdown logic."""
        self.is_running = False
        logger.info("ORCHESTRATOR: Shutdown signal received.")

main_orchestrator = SwarmOrchestrator()