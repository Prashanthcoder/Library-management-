"""
routers/books.py
----------------
BOOK CRUD ENDPOINTS

PASTE LOCATION: library_system/routers/books.py  (replace the whole file)

Fix: delete endpoint now checks for active transactions before allowing deletion.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookResponse, status_code=201)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """Add a new book. Requires login."""
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """Return all books. Requires login."""
    return db.query(models.Book).all()


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    updates: schemas.BookUpdate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """Update book details. Requires login."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user)
):
    """
    Delete a book. Requires login.

    Blocks deletion if the book has any unreturned (active) transactions —
    you can't remove a book that is currently issued to a member.

    Books with only fully-returned transaction history CAN be deleted.
    Their historical transaction records are also removed to keep the DB clean.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check for active (unreturned) transactions
    active_txn = db.query(models.Transaction).filter(
        models.Transaction.book_id == book_id,
        models.Transaction.return_date == None   # noqa: E711
    ).first()

    if active_txn:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Cannot delete this book — it is currently issued to a member. "
                "Please ensure all copies are returned before deleting."
            )
        )

    # Safe to delete: remove completed transaction history first, then the book
    db.query(models.Transaction).filter(
        models.Transaction.book_id == book_id
    ).delete(synchronize_session=False)

    db.delete(book)
    db.commit()
