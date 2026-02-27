from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    assigned_to = Column(String, nullable=True)
    status = Column(String)
    payload = Column(Text)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
