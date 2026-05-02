from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.models.base import Base

class Memorial(Base):
    __tablename__ = "memorials"
    __table_args__ = {"schema": "tenant_1"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    happened_at = Column(DateTime, nullable=True)
    images = Column(JSON, default=list)  # 存储图片URL数组
    created_at = Column(DateTime, server_default=func.now())