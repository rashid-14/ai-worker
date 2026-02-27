from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    task_type = Column(String, nullable=False)

    assigned_to = Column(String, nullable=True)

    status = Column(String, default="new")

    payload = Column(Text, nullable=True)

    result = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
