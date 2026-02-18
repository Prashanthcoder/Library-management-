# 📚 Library Management System

A full-stack Library Management System built with **FastAPI** + **SQLite** on the backend
and pure **HTML/CSS/JavaScript** on the frontend.

---

## Project Structure

```
library_system/
├── main.py               # FastAPI app entry point
├── database.py           # SQLAlchemy engine + session dependency
├── models.py             # ORM table definitions (Book, Member, Transaction)
├── schemas.py            # Pydantic request/response schemas
├── requirements.txt
├── routers/
│   ├── books.py          # CRUD endpoints for books
│   ├── members.py        # Member registration endpoints
│   └── transactions.py   # Issue / return book endpoints
├── static/
│   ├── style.css         # Dashboard styles
│   └── script.js         # Fetch API calls + DOM updates
└── templates/
    └── index.html        # Single-page dashboard
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
cd library_system
uvicorn main:app --reload
```

### 3. Open the dashboard

```
http://localhost:8000
```

### 4. Explore the API docs

FastAPI auto-generates interactive docs:

```
http://localhost:8000/docs
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /books/ | Add a book |
| GET | /books/ | List all books |
| PUT | /books/{id} | Update a book |
| DELETE | /books/{id} | Delete a book |
| POST | /members/ | Register a member |
| GET | /members/ | List all members |
| POST | /transactions/issue | Issue a book |
| PUT | /transactions/return/{id} | Return a book |
| GET | /transactions/ | List active (unreturned) issues |

---

## Architecture Notes

- **Dependency Injection**: `get_db()` in `database.py` is injected via `Depends()` into every router that needs a DB session — no globals, easy to test.
- **Separation of Concerns**: Models (ORM) are separate from Schemas (Pydantic) — API contracts don't leak DB internals.
- **Quantity Guard**: The issue endpoint checks `book.quantity > 0` before allowing issue, and atomically decrements/increments it.
- **Frontend**: Pure vanilla JS with `fetch()` — no build step, no frameworks. The entire UI updates reactively after each action.