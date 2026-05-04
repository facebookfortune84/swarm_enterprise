import logging
from backend.db.linear_engine import swarm_db
from backend.db.models import Project, Ticket, TicketStatus

# Setup professional logging for the ignition sequence
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DB_Seed")

def seed_factory():
    """
    Initializes the Sovereign Factory.
    Creates the 'Launch Audit' project which triggers the 12-manager board
    to verify the 44 manifest files and SOP compliance.
    """
    session = swarm_db.Session()
    try:
        project_count = session.query(Project).count()
        
        if project_count == 0:
            logger.info("SEEDER: Database is empty. Initiating Sovereign Genesis...")
            
            # 1. Create the Genesis Project
            project_id = swarm_db.create_project(
                name="Swarm OS v1.0 Launch Audit",
                description=(
                    "Perform a full-scale fractal audit of the Swarm Enterprise infrastructure. "
                    "1. Verify all 44 manifest files are physically readable. "
                    "2. Ensure SHA-256 headers are being injected correctly. "
                    "3. Validate the 12-manager strategic handoff to supervisors."
                ),
                tech_stack="Fractal Sovereign Stack (Groq/Ollama)"
            )
            
            # 2. Create the Root Ticket
            # This ticket is assigned to 'USER' so the Orchestrator knows 
            # to hand it to the Board (Level 1) first.
            swarm_db.create_ticket(
                project_id=project_id,
                title="SOP & Infrastructure Compliance Check",
                instruction=(
                    "Analyze the current /sops and /backend directories. "
                    "Confirm every agent is operating within constitutional limits. "
                    "Output a 36-ticket plan to refine any detected drift."
                ),
                creator_role="USER",
                assigned_role="BOARD_OF_DIRECTORS"
            )
            
            logger.info(f"SEEDER: Genesis successful. Project {project_id} is now in the queue.")
        else:
            logger.info(f"SEEDER: {project_count} projects detected. System state preserved.")
            
    except Exception as e:
        logger.error(f"SEEDER_CRITICAL_FAILURE: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_factory()