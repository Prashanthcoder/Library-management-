"""
routers/auth.py
---------------
AUTHENTICATION ENDPOINTS  (NEW FILE)

Routes:
  POST /auth/signup   → create account, return JWT
  POST /auth/login    → verify credentials, return JWT
  GET  /auth/me       → return current user info (protected)

PASTE LOCATION: library_system/routers/auth.py  (create this new file)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from auth import hash_password, verify_password, create_access_token, get_current_user
import models
import schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=schemas.TokenResponse, status_code=201)
def signup(payload: schemas.UserSignup, db: Session = Depends(get_db)):
    """
    Register a new librarian account.

    - Checks username and email are not already taken
    - Hashes the password with bcrypt
    - Returns a JWT so the user is immediately logged in
    """
    # Check duplicate username
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken. Please choose another."
        )

    # Check duplicate email
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    # Create user with hashed password
    user = models.User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Return a token so frontend can log in immediately after signup
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a librarian.

    - Looks up the user by username
    - Verifies the password against the stored bcrypt hash
    - Returns a signed JWT valid for 8 hours
    """
    user = db.query(models.User).filter(
        models.User.username == payload.username).first()

    # Use same error for "not found" and "wrong password" to prevent username enumeration
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated."
        )

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """
    Return the currently logged-in user's profile.
    This route is protected — requires a valid Bearer token.
    """
    return current_user
