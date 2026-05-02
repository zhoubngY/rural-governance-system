from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class Notice(Base):
    __tablename__ = "notices"
    __table_args__ = {"schema": "tenant_1"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_top = Column(Boolean, default=False)
    published_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())