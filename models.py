"""
models.py
---------
DATABASE TABLES (SQLAlchemy ORM)

Tables defined here:
  - User         ← NEW: stores librarian accounts
  - Book
  - Member
  - Transaction

PASTE LOCATION: library_system/models.py  (replace the whole file)
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime


# ─────────────────────────────────────────
# NEW: User model for authentication
# ─────────────────────────────────────────
class User(Base):
    """
    Librarian / admin account.
    Passwords are stored as bcrypt hashes — never plain text.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)


class Book(Base):
    """Represents a book in the library catalog."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    transactions = relationship("Transaction", back_populates="book")


class Member(Base):
    """Represents a registered library member."""
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    transactions = relationship("Transaction", back_populates="member")


class Transaction(Base):
    """Tracks book issue and return events."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"),    nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    issue_date = Column(Date, default=datetime.date.today, nullable=False)
    return_date = Column(Date, nullable=True)

    book = relationship("Book",   back_populates="transactions")
    member = relationship("Member", back_populates="transactions")
