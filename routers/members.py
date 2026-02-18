"""
routers/members.py
------------------
All endpoints related to library members:
  POST   /members/  - Register a new member
  GET    /members/  - List all members
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=schemas.MemberResponse, status_code=status.HTTP_201_CREATED)
def register_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    """Register a new library member."""
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=List[schemas.MemberResponse])
def get_all_members(db: Session = Depends(get_db)):
    """Return all registered members."""
    return db.query(models.Member).all()
