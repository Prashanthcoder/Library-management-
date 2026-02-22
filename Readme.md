<div align="center">

<br/>

<!-- Claude-style logo using SVG -->
<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#f97316"/>
      <stop offset="25%"  stop-color="#ec4899"/>
      <stop offset="50%"  stop-color="#8b5cf6"/>
      <stop offset="75%"  stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <circle cx="40" cy="40" r="38" fill="url(#g1)"/>
  <circle cx="40" cy="40" r="24" fill="white"/>
  <text x="40" y="47" text-anchor="middle" font-size="20">📚</text>
</svg>

# Library Management System

**A full-stack Library Management System built with FastAPI + SQLite + Vanilla JS**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

[Features](#-features) • [Demo](#-screenshots) • [Quick Start](#-quick-start) • [API Docs](#-api-reference) • [Project Structure](#-project-structure) • [Auth Flow](#-authentication-flow)

</div>

---

##  Features

- 🔐 **JWT Authentication** — Secure signup/login with bcrypt password hashing
- 📖 **Book Catalog** — Add, update, delete and list books with quantity tracking
- 👥 **Member Management** — Register and manage library members
- 🔄 **Transactions** — Issue and return books with automatic quantity adjustment
- 🛡️ **Protected Routes** — All API endpoints require a valid JWT token
- 🎨 **Modern UI** — Clean single-page dashboard with toast notifications
- ✅ **Login Animation** — Smooth SVG checkmark success animation on login
- 📱 **Responsive** — Works on desktop and mobile
- 📄 **Auto Docs** — Swagger UI at `/docs` with JWT Authorize button

---

##  Screenshots

| Login Page | Dashboard |
|-----------|-----------|
|  Animated logo, smooth post-login animation | Books, members, and transactions in one view |

---

##  Quick Start

### Prerequisites

- Python 3.11+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/yourname/library-management-system.git
cd library-management-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

### 4. Open in browser

| Page | URL |
|------|-----|
| Signup | http://localhost:8000/signup |
| Login | http://localhost:8000/login |
| Dashboard | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

> The dashboard automatically redirects to `/login` if you are not authenticated.

---

##  Project Structure

```
library-management-system/
│
├── main.py                  # FastAPI app entry point, route registration
├── database.py              # SQLAlchemy engine, session factory, get_db()
├── models.py                # ORM table definitions (User, Book, Member, Transaction)
├── schemas.py               # Pydantic request/response schemas with validation
├── auth.py                  # JWT utilities, bcrypt hashing, get_current_user()
├── requirements.txt         # Python dependencies
│
├── routers/
│   ├── auth.py              # POST /auth/signup, /auth/login, GET /auth/me
│   ├── books.py             # CRUD /books/
│   ├── members.py           # POST /members/, GET /members/
│   └── transactions.py      # POST /transactions/issue, PUT /transactions/return/{id}
│
├── static/
│   ├── style.css            # Dashboard styles
│   ├── auth.css             # Login/signup page styles + success animation
│   └── script.js            # Fetch API calls, JWT handling, DOM updates
│
└── templates/
    ├── index.html           # Main dashboard (protected)
    ├── login.html           # Login page with post-login animation
    └── signup.html          # Signup page with password strength rules
```

---

## 🗄️ Database Models

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│    Book     │     │  Transaction │     │     Member      │
├─────────────┤     ├──────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ book_id (FK) │────►│ id (PK)         │
│ title       │     │ member_id(FK)│     │ name            │
│ author      │     │ id (PK)      │     └─────────────────┘
│ quantity    │     │ issue_date   │
└─────────────┘     │ return_date  │     ┌─────────────────┐
                    └──────────────┘     │      User       │
                                         ├─────────────────┤
                                         │ id (PK)         │
                                         │ username        │
                                         │ email           │
                                         │ hashed_password │
                                         │ is_active       │
                                         └─────────────────┘
```

---

##  API Reference

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/signup` | Register a new librarian account | 
| `POST` | `/auth/login` | Login and receive JWT token | 
| `GET` | `/auth/me` | Get current logged-in user | 

### Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/books/` | Add a new book to catalog | 
| `GET` | `/books/` | List all books | 
| `PUT` | `/books/{id}` | Update book details | 
| `DELETE` | `/books/{id}` | Delete a book (blocks if issued) | 

### Members

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/members/` | Register a new member | 
| `GET` | `/members/` | List all members | 

### Transactions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/transactions/issue` | Issue a book to a member |
| `PUT` | `/transactions/return/{id}` | Return a book |
| `GET` | `/transactions/` | List all currently issued books  |

---

##  Authentication Flow

```
┌─────────┐        POST /auth/login         ┌─────────┐
│ Browser │ ──────────────────────────────► │  FastAPI │
│         │   {username, password}          │         │
│         │ ◄────────────────────────────── │         │
│         │   {access_token: "eyJ..."}      └────┬────┘
│         │                                      │ bcrypt verify
│  stores │                                      │ jwt.encode()
│  token  │                                      ▼
│   in    │        GET /books/               ┌─────────┐
│ local   │ ──────────────────────────────► │  FastAPI │
│ Storage │  Authorization: Bearer eyJ...   │         │
│         │ ◄────────────────────────────── │         │
│         │   [{id:1, title:"..."}]         └────┬────┘
└─────────┘                                      │ jwt.decode()
                                                 │ get_current_user()
                                                 ▼
                                          Returns User row
                                          or 401 Unauthorized
```

### Using Swagger UI with JWT

1. Go to **http://localhost:8000/docs**
2. Call `POST /auth/login` → copy the `access_token`
3. Click ** Authorize** at the top
4. Enter `Bearer <your_token>` → click Authorize
5. All protected endpoints are now unlocked

---

##  Environment & Configuration

The following constants in `auth.py` can be changed:

```python
# auth.py
SECRET_KEY = "library-super-secret-key-change-in-production"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480   # 8 hours
```

> **For production**: load `SECRET_KEY` from an environment variable:
> ```python
> import os
> SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-dev-key")
> ```

---

##  Bugs Fixed During Development

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError: cannot import from partially initialized module 'auth'` | `auth.py` was importing from itself (circular import) | Removed the self-import line from `auth.py` |
| `ValueError: password cannot be longer than 72 bytes` | bcrypt 4.x strict limit, no validation before hashing | Added `@field_validator` in `UserSignup` schema, capped at 64 chars |
| `AttributeError: module 'bcrypt' has no attribute '__about__'` | `passlib 1.7.4` incompatible with `bcrypt 4.1+` | Pinned `bcrypt==4.0.1` in requirements |
| `IntegrityError: NOT NULL constraint failed: transactions.book_id` | SQLAlchemy nullified FK on delete instead of blocking | Block delete if active transactions exist, cascade delete history only |

---

##  Dependencies

```
fastapi==0.111.0          # Web framework
uvicorn==0.29.0           # ASGI server
sqlalchemy==2.0.30        # ORM
pydantic==2.7.1           # Data validation
python-jose[cryptography] # JWT encoding/decoding
passlib[bcrypt]==1.7.4    # Password hashing
bcrypt==4.0.1             # Pinned for passlib compatibility
python-multipart==0.0.9   # Form data parsing
```

---

##  Security Notes

| Topic | Current | Production Recommendation |
|-------|---------|--------------------------|
| Password storage | bcrypt (10 rounds) |  Good as-is |
| Token secret | Hardcoded string |  Use environment variable |
| Token storage | `localStorage` | Consider `httpOnly` cookies |
| HTTPS | Not configured | Use nginx reverse proxy with TLS |
| Token expiry | 8 hours | Adjust based on use case |

---

##  Git Commit History

```bash
feat: initial library management system with books, members, transactions
feat(auth): add JWT authentication with bcrypt password hashing
feat(ui): add login and signup pages with Claude-style animated logo
feat(security): protect all API routes with JWT bearer token
fix: pin bcrypt==4.0.1 and add password length validation (6-64 chars)
fix: block book deletion if active transactions exist, cascade delete history
feat(ui): add post-login success animation with SVG checkmark and overlay
```

---

##  License

This project is licensed under the MIT License.

---
