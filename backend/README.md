# Interactive Web Novels - Backend API

FastAPI backend for the Interactive Web Novels platform.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)

## Setup Instructions

### 1. Install PostgreSQL

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Default port is 5432

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

Open PostgreSQL command line (psql) or use pgAdmin:

```sql
CREATE DATABASE interactive_novels;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE interactive_novels TO your_username;
```

### 3. Set Up Python Virtual Environment

Navigate to the backend directory:

```bash
cd backend
```

Create virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and update the values:
   - `DATABASE_URL`: Update with your PostgreSQL credentials
   - `SECRET_KEY`: Generate a secure key (run: `openssl rand -hex 32`)

### 6. Run Database Migrations

Initialize the database schema using Alembic:

```bash
alembic upgrade head
```

### 7. Run the Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       ├── endpoints/  # Individual endpoint modules
│   │       └── api.py      # Router aggregation
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── security.py   # Auth utilities
│   ├── db/               # Database configuration
│   │   ├── base.py       # Model imports for Alembic
│   │   ├── base_class.py # SQLAlchemy base class
│   │   └── session.py    # Database session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── uploads/              # File uploads (gitignored)
├── .env                  # Environment variables (gitignored)
├── .env.example          # Example environment variables
├── alembic.ini           # Alembic configuration
├── main.py               # FastAPI application entry point
└── requirements.txt      # Python dependencies
```

## Development

### Running Tests

```bash
pytest
```

### Creating a New Migration

After modifying models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. Install it: `pip install -r requirements.txt`

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Issues

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Ensure database and user exist

### Port Already in Use
- Change the port: `uvicorn main:app --reload --port 8001`

### Module Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

- [ ] Phase 1.2: User Authentication System
- [ ] Phase 1.3: Books Management API
- [ ] Phase 1.4: Chapters Management API

