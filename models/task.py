from sqlalchemy import Column, Integer, String, JSON, DateTime
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    assigned_to = Column(String)
    status = Column(String, default="pending")
    payload = Column(JSON)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
