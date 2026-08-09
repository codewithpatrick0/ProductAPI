# ProductAPI

A notes API with JWT-based authentication, built with **FastAPI**, **SQLAlchemy**, and **Alembic** migrations. This is a mini project made to consolidate core backend concepts (auth flows, migrations, and layered app structure) before moving on to larger projects.

## Features

- User registration and login with hashed passwords (`pwdlib`)
- JWT access/refresh tokens delivered via HTTP-only cookies
- Token refresh endpoint
- CRUD endpoints for notes, scoped to the authenticated user
- Database migrations with Alembic
- Minimal HTML/JS frontend for manual testing

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [pwdlib](https://frankie567.github.io/pwdlib/) (Argon2 password hashing)
- SQLite

## Project structure

```
.
├── main.py           # FastAPI app entry point
├── routes/            # API routes (auth, notes)
├── crud/               # Database operations
├── models/             # SQLAlchemy ORM models
├── schemes/             # Pydantic schemas for request/response validation
├── database/             # Database engine and session configuration
├── security/               # Password hashing and JWT helpers
├── alembic/                 # Database migrations
└── frontend/                 # Static HTML/JS pages for manual testing
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/codewithpatrick0/ProductAPI.git
cd ProductAPI
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own secret keys:

```bash
cp .env.example .env
```

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
REFRESH_KEY=your_refresh_secret_key
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and the interactive docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Auth

| Method | Endpoint        | Description                  |
|--------|-----------------|-------------------------------|
| POST   | `/auth/register`| Register a new user           |
| POST   | `/auth/login`    | Log in and receive JWT cookies|
| POST   | `/auth/refresh`  | Refresh the access token      |

### Notes (require authentication)

| Method | Endpoint          | Description        |
|--------|-------------------|---------------------|
| POST   | `/notes/`         | Create a new note   |
| GET    | `/notes/`         | List the user's notes |
| GET    | `/notes/{note_id}`| Get a single note   |
| PATCH  | `/notes/{note_id}`| Edit a note         |
| DELETE | `/notes/{note_id}`| Delete a note       |
