"""
models.py
---------
Defines the database tables using SQLAlchemy ORM.
Each class maps to one table in library.db.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Book(Base):
    """Represents a book in the library catalog."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    # One book can have many transactions
    transactions = relationship("Transaction", back_populates="book")


class Member(Base):
    """Represents a registered library member."""
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    # One member can have many transactions
    transactions = relationship("Transaction", back_populates="member")


class Transaction(Base):
    """Tracks book issue and return events."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    issue_date = Column(Date, default=datetime.date.today, nullable=False)
    return_date = Column(Date, nullable=True)  # NULL means not yet returned

    # Relationships for easy access to related objects
    book = relationship("Book", back_populates="transactions")
    member = relationship("Member", back_populates="transactions")
