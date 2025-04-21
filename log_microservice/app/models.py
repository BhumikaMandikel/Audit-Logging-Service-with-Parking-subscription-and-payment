
from sqlalchemy import Column, Integer, String, JSON, DateTime
from .database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(100), index=True)
    user_id = Column(String(100), index=True)
    action = Column(String(100), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)
