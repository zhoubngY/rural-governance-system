from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "tenant_1"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")
    due_date = Column(String(50), nullable=True)
    extra_data = Column(JSON, default=dict)
    status = Column(String(20), default="pending")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee_ids = Column(JSON, default=list)  # 多负责人ID数组
    assigned_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    assigned_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    result_note = Column(Text)