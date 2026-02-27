from sqlalchemy import Column, Integer, String, DateTime, JSON
from database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String, nullable=True)
    assigned_to = Column(String, nullable=True)
    status = Column(String, default="new")
    payload = Column(JSON)   # ✅ Must be JSON
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
