import hashlib
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from sqlalchemy import create_engine, update, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, Project, Ticket, AuditLog, TicketStatus, RiskLevel

# Database path must be consistent with docker-compose volume mapping
DB_PATH = "sqlite:////app/swarm_tickets.db"

# Configure database-level logging
logger = logging.getLogger("LinearEngine")

class LinearEngine:
    """
    The Industrial-Grade Ticketing Engine.
    Manages the lifecycle of fractal tasks with strict adherence to 
    the Swarm Constitution (SOPs 01-08).
    """

    def __init__(self):
        self.engine = create_engine(
            DB_PATH,
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    # --- 1. PROJECT LIFECYCLE ---
    def create_project(self, name: str, description: str, tech_stack: str) -> str:
        """Initializes a new enterprise build in the database."""
        session = self.Session()
        try:
            project_id = f"PROJ-{uuid.uuid4().hex[:6].upper()}"
            new_project = Project(
                id=project_id,
                name=name,
                description=description,
                tech_stack=tech_stack
            )
            session.add(new_project)
            session.commit()
            logger.info(f"PROJECT_CREATED: {project_id} - {name}")
            return project_id
        except Exception as e:
            session.rollback()
            logger.error(f"PROJECT_ERROR: {e}")
            raise e

    # --- 2. FRACTAL TICKET LOGIC ---
    def create_ticket(self, project_id, title, instruction, creator_role, assigned_role, parent_id=None):
        session = self.Session()
        try:
            ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
            new_ticket = Ticket(
                id=ticket_id,
                project_id=project_id,
                parent_id=parent_id,
                creator_role=creator_role,
                assigned_role=assigned_role,
                title=title,
                instruction=instruction,
                status=TicketStatus.OPEN
            )
            session.add(new_ticket)
            session.commit()
            return ticket_id
        except Exception as e:
            session.rollback()
            return None

    def claim_ticket(self, ticket_id: str, agent_role: str):
        session = self.Session()
        session.query(Ticket).filter(Ticket.id == ticket_id).update({
            "status": TicketStatus.CLAIMED,
            "assigned_role": agent_role,
            "updated_at": datetime.utcnow()
        })
        session.commit()

    def submit_work(self, ticket_id: str, file_path: str, content: str):
        session = self.Session()
        file_hash = hashlib.sha256(content.encode()).hexdigest()
        session.query(Ticket).filter(Ticket.id == ticket_id).update({
            "status": TicketStatus.REVIEW_REQUIRED,
            "file_path": file_path,
            "sha256_hash": file_hash,
            "updated_at": datetime.utcnow()
        })
        session.commit()
        return file_hash

    # --- 3. ADVERSARIAL AUDIT & SECURITY ---
    def log_audit(self, ticket_id: str, auditor_role: str, risk: str, action: str, findings: str):
        session = self.Session()
        try:
            risk_enum = RiskLevel[risk.upper()]
            new_audit = AuditLog(
                ticket_id=ticket_id,
                auditor_role=auditor_role,
                action_taken=action,
                findings=findings
            )
            session.add(new_audit)
            
            # Update Ticket based on Audit
            status = TicketStatus.VERIFIED if action == "APPROVED" else TicketStatus.REJECTED
            session.query(Ticket).filter(Ticket.id == ticket_id).update({
                "status": status,
                "risk_assessment": risk_enum,
                "updated_at": datetime.utcnow()
            })
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"AUDIT_ERROR: {e}")

    # --- 4. ANALYTICS ---
    def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        session = self.Session()
        tickets = session.query(Ticket).filter(Ticket.project_id == project_id).all()
        return {
            "total": len(tickets),
            "completed": len([t for t in tickets if t.status == TicketStatus.COMPLETED]),
            "verified": len([t for t in tickets if t.status == TicketStatus.VERIFIED]),
            "rejected": len([t for t in tickets if t.status == TicketStatus.REJECTED])
        }

    def close(self):
        self.Session.remove()

swarm_db = LinearEngine()