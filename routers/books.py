"""
routers/books.py
----------------
All endpoints related to book management:
  POST   /books/         - Add a book
  GET    /books/         - List all books
  PUT    /books/{id}     - Update a book
  DELETE /books/{id}     - Delete a book
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library catalog."""
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """Return all books in the library."""
    return db.query(models.Book).all()


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, updates: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update book details. Only provided fields will be changed."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Apply only the fields that were provided in the request
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Remove a book from the catalog."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
