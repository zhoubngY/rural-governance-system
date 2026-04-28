from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.models.base import Base

class WorkNote(Base):
    __tablename__ = "work_notes"
    __table_args__ = {"schema": "tenant_1"}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    user_id = Column(Integer, nullable=False)   # 移除外键声明
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())