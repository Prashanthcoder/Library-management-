"""
main.py
-------
APPLICATION ENTRY POINT

Changes from original:
  - Added auth router
  - Added routes to serve login.html and signup.html
  - Swagger UI now shows the Authorize button for JWT

PASTE LOCATION: library_system/main.py  (replace the whole file)
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi

from database import engine, Base
import models   # ensures all models registered before create_all
from routers import books, members, transactions
from routers import auth as auth_router

# Create all tables (including the new `users` table)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="""
## Library Management API with JWT Authentication

### Auth Flow
1. **POST /auth/signup** — create account → get token
2. **POST /auth/login**  — log in → get token
3. Click **Authorize** (🔒) above and paste:  `Bearer <your_token>`
4. All other endpoints are now unlocked

### Endpoints
- **Books** — CRUD operations on the catalog
- **Members** — register and list library members
- **Transactions** — issue and return books
    """,
    version="2.0.0"
)

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(auth_router.router)    # /auth/signup, /auth/login, /auth/me
app.include_router(books.router)          # /books/
app.include_router(members.router)        # /members/
app.include_router(transactions.router)   # /transactions/


# ── Page routes ──────────────────────────

@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Main dashboard — redirects to login if no token present (handled client-side)."""
    return FileResponse("templates/index.html")


@app.get("/login", include_in_schema=False)
def serve_login():
    return FileResponse("templates/login.html")


@app.get("/signup", include_in_schema=False)
def serve_signup():
    return FileResponse("templates/signup.html")
