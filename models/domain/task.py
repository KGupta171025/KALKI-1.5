from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime, Float
from database.postgres import Base
import datetime

class TaskModel(Base):
    """
    SQLAlchemy task model mapping relational database schema.
    """
    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True, index=True)
    session_id = Column(String(50), nullable=False)
    goal = Column(String(500), nullable=False)
    status = Column(String(20), default="PENDING") # PENDING, RUNNING, SUCCESS, FAILED
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
