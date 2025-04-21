
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, models, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log", response_model=schemas.LogOut)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = models.AuditLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/logs", response_model=list[schemas.LogOut])
def get_logs(service: str = "", user_id: str = "", db: Session = Depends(get_db)):
    query = db.query(models.AuditLog)
    if service:
        query = query.filter(models.AuditLog.service == service)
    if user_id:
        query = query.filter(models.AuditLog.user_id == user_id)
    return query.all()
