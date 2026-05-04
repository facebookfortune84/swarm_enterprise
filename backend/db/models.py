from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    REVIEW_REQUIRED = "review_required"
    REJECTED = "rejected"
    VERIFIED = "verified"
    COMPLETED = "completed"

class RiskLevel(str, enum.Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    MEDIUM_HIGH = "medium_high"
    HIGH = "high"

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tech_stack = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    tickets = relationship("Ticket", back_populates="project")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    parent_id = Column(String, ForeignKey("tickets.id"), nullable=True)
    creator_role = Column(String)
    assigned_role = Column(String)
    title = Column(String, nullable=False)
    instruction = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    risk_assessment = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    file_path = Column(String, nullable=True)
    sha256_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project = relationship("Project", back_populates="tickets")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(String, ForeignKey("tickets.id"))
    auditor_role = Column(String)
    action_taken = Column(String)
    findings = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)