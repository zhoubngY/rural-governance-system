from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class NoteType(str, enum.Enum):
    VEHICLE = "vehicle"
    ENGINEERING = "engineering"
    LABOR = "labor"
    OTHER = "other"
    MEMO = "memo"

class WorkNote(Base):
    __tablename__ = "work_notes"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NoteType), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    extra_data = Column(Text)
