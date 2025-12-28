from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import models
from pydantic import BaseModel
from datetime import date

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for response
class VulnerabilityOut(BaseModel):
    id: int
    cve_id: str
    software_name: str
    affected_version: str
    severity: str
    patch_command: str
    published_date: date | None

    class Config:
        from_attributes = True

@router.get("/vulnerabilities", response_model=List[VulnerabilityOut])
def get_vulnerabilities(db: Session = Depends(get_db)):
    return db.query(models.Vulnerability).all()

@router.get("/status")
def get_status():
    return {"status": "Active", "mode": "Continuous Scanning"}
