
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class LogCreate(BaseModel):
    service: str
    user_id: str
    action: str
    details: Optional[Dict]

class LogOut(LogCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
