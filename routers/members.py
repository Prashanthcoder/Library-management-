"""
routers/members.py
------------------
MEMBER ENDPOINTS (protected)

PASTE LOCATION: library_system/routers/members.py  (replace the whole file)
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=schemas.MemberResponse, status_code=201)
def register_member(
    member: schemas.MemberCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """Register a new library member. Requires login."""
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=List[schemas.MemberResponse])
def get_all_members(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """Return all registered members. Requires login."""
    return db.query(models.Member).all()
