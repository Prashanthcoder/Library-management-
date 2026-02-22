"""
schemas.py
----------
PYDANTIC REQUEST / RESPONSE MODELS

PASTE LOCATION: library_system/schemas.py  (replace the whole file)
"""

from pydantic import BaseModel, field_validator
from typing import Optional
import datetime


# ──────────────────────────────────────────
# AUTH SCHEMAS
# ──────────────────────────────────────────

class UserSignup(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def password_rules(cls, v):
        """
        Validate password before it ever reaches bcrypt.
        bcrypt hard limit is 72 bytes — we enforce 64 chars max to stay safe.
        """
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if len(v) > 64:
            raise ValueError("Password must be 64 characters or fewer.")
        return v

    @field_validator("username")
    @classmethod
    def username_rules(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if len(v) > 50:
            raise ValueError("Username must be 50 characters or fewer.")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# BOOK SCHEMAS
# ──────────────────────────────────────────

class BookCreate(BaseModel):
    title:    str
    author:   str
    quantity: int = 1


class BookUpdate(BaseModel):
    title:    Optional[str] = None
    author:   Optional[str] = None
    quantity: Optional[int] = None


class BookResponse(BaseModel):
    id:       int
    title:    str
    author:   str
    quantity: int

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# MEMBER SCHEMAS
# ──────────────────────────────────────────

class MemberCreate(BaseModel):
    name: str


class MemberResponse(BaseModel):
    id:   int
    name: str

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# TRANSACTION SCHEMAS
# ──────────────────────────────────────────

class IssueBookRequest(BaseModel):
    book_id:   int
    member_id: int


class TransactionResponse(BaseModel):
    id:          int
    book_id:     int
    member_id:   int
    issue_date:  datetime.date
    return_date: Optional[datetime.date] = None
    book_title:  Optional[str] = None
    member_name: Optional[str] = None

    model_config = {"from_attributes": True}
