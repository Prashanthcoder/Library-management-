"""
schemas.py
----------
Pydantic schemas for request validation and response serialization.
Keeps API contracts clearly separate from database models.
"""

from pydantic import BaseModel
from typing import Optional
import datetime


# ──────────────────────────────────────────
# BOOK SCHEMAS
# ──────────────────────────────────────────

class BookCreate(BaseModel):
    """Payload for creating a new book."""
    title: str
    author: str
    quantity: int = 1


class BookUpdate(BaseModel):
    """Payload for updating an existing book (all fields optional)."""
    title: Optional[str] = None
    author: Optional[str] = None
    quantity: Optional[int] = None


class BookResponse(BaseModel):
    """What the API returns when representing a book."""
    id: int
    title: str
    author: str
    quantity: int

    model_config = {"from_attributes": True}  # Allows ORM object → Pydantic


# ──────────────────────────────────────────
# MEMBER SCHEMAS
# ──────────────────────────────────────────

class MemberCreate(BaseModel):
    """Payload for registering a new member."""
    name: str


class MemberResponse(BaseModel):
    """What the API returns when representing a member."""
    id: int
    name: str

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# TRANSACTION SCHEMAS
# ──────────────────────────────────────────

class IssueBookRequest(BaseModel):
    """Payload for issuing a book to a member."""
    book_id: int
    member_id: int


class TransactionResponse(BaseModel):
    """What the API returns for a transaction."""
    id: int
    book_id: int
    member_id: int
    issue_date: datetime.date
    return_date: Optional[datetime.date] = None
    # Nested details for richer frontend display
    book_title: Optional[str] = None
    member_name: Optional[str] = None

    model_config = {"from_attributes": True}
