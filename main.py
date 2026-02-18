"""
main.py
-------
Application entry point.
- Creates all DB tables on startup
- Mounts static files
- Registers all routers
- Serves the frontend HTML
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine, Base
import models  # noqa: F401 — ensures models are registered with Base before create_all
from routers import books, members, transactions

# Create all database tables (safe to call even if tables already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="A simple REST API for managing library books, members and loans",
    version="1.0.0"
)

# Serve CSS and JS from /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routers with their prefixes
app.include_router(books.router)
app.include_router(members.router)
app.include_router(transactions.router)


@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve the single-page frontend."""
    return FileResponse("templates/index.html")
