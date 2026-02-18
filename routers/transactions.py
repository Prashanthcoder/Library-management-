"""
routers/transactions.py
-----------------------
All endpoints related to book transactions:
  POST  /transactions/issue/{id}   - Issue a book to a member
  PUT   /transactions/return/{id}  - Return a book
  GET   /transactions/             - List all active (unreturned) transactions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from database import get_db
import models
import schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/issue", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def issue_book(payload: schemas.IssueBookRequest, db: Session = Depends(get_db)):
    """
    Issue a book to a member.
    - Checks the book exists and has copies available (quantity > 0)
    - Decrements the book's quantity by 1
    - Records the transaction with today's date
    """
    # Validate book exists
    book = db.query(models.Book).filter(
        models.Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check copies are available
    if book.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No copies of this book are currently available"
        )

    # Validate member exists
    member = db.query(models.Member).filter(
        models.Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Decrement available quantity
    book.quantity -= 1

    # Create transaction record
    transaction = models.Transaction(
        book_id=payload.book_id,
        member_id=payload.member_id,
        issue_date=datetime.date.today()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Build enriched response with book and member names
    return schemas.TransactionResponse(
        id=transaction.id,
        book_id=transaction.book_id,
        member_id=transaction.member_id,
        issue_date=transaction.issue_date,
        return_date=transaction.return_date,
        book_title=book.title,
        member_name=member.name
    )


@router.put("/return/{transaction_id}", response_model=schemas.TransactionResponse)
def return_book(transaction_id: int, db: Session = Depends(get_db)):
    """
    Return a book.
    - Marks return_date as today
    - Increments the book's quantity by 1
    """
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if transaction.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book has already been returned"
        )

    # Mark as returned and restore quantity
    transaction.return_date = datetime.date.today()
    transaction.book.quantity += 1

    db.commit()
    db.refresh(transaction)

    return schemas.TransactionResponse(
        id=transaction.id,
        book_id=transaction.book_id,
        member_id=transaction.member_id,
        issue_date=transaction.issue_date,
        return_date=transaction.return_date,
        book_title=transaction.book.title,
        member_name=transaction.member.name
    )


@router.get("/", response_model=List[schemas.TransactionResponse])
def get_active_transactions(db: Session = Depends(get_db)):
    """Return all transactions where the book hasn't been returned yet."""
    transactions = db.query(models.Transaction).filter(
        models.Transaction.return_date == None
    ).all()

    return [
        schemas.TransactionResponse(
            id=t.id,
            book_id=t.book_id,
            member_id=t.member_id,
            issue_date=t.issue_date,
            return_date=t.return_date,
            book_title=t.book.title,
            member_name=t.member.name
        )
        for t in transactions
    ]
