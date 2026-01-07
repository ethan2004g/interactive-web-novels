# Quick Fix: Database Setup for Create Book Feature

## Issue
The "Create Book" feature isn't saving because the database isn't properly set up.

## Solution Steps

### Step 1: Check PostgreSQL is Running

**Open Windows Services:**
1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Look for "postgresql-x64-14" (or similar)
4. Make sure it's running (Status: Running)
5. If not, right-click and select "Start"

**OR Check via Command:**
```powershell
Get-Service postgresql*
```

### Step 2: Create/Verify Database

**Option A: Using pgAdmin (Graphical)**
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to your PostgreSQL server
3. Right-click "Databases" → Create → Database
4. Name: `interactive_novels`
5. Click Save

**Option B: Using Command Line (psql)**
```powershell
# Connect to PostgreSQL (you'll be prompted for password)
psql -U postgres

# In the psql prompt:
CREATE DATABASE interactive_novels;
\l                    # List databases to verify
\q                    # Quit
```

### Step 3: Run Database Migrations

**Open a NEW terminal in the backend folder:**

```powershell
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run migrations to create tables
alembic upgrade head
```

**You should see output like:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 4864b457d68d, add users table
INFO  [alembic.runtime.migration] Running upgrade 4864b457d68d -> 3fd1f6253b18, add books table
INFO  [alembic.runtime.migration] Running upgrade 3fd1f6253b18 -> 5c7e9f8d2a3b, add chapters table
...
```

### Step 4: Restart Backend Server

**Stop the current server** (Ctrl+C in the backend terminal)

Then restart it **with venv activated:**

```powershell
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

You should see:
```
INFO:     Application startup complete.
```

### Step 5: Test Create Book

1. Go to http://localhost:3000
2. Login as an author
3. Go to Dashboard → My Books → Create New Book
4. Fill out the form and click "Create Book"
5. Should redirect to edit page successfully!

---

## Troubleshooting

### Error: "password authentication failed"

Your database credentials don't match. Check your `.env` file:

```powershell
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"
notepad .env
```

Update the `DATABASE_URL` line:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/interactive_novels
```

Replace `YOUR_PASSWORD` with your PostgreSQL password (set during installation).

### Error: "database does not exist"

Run Step 2 above to create the database.

### Error: "No module named 'sqlalchemy'"

You need to activate the virtual environment:
```powershell
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"
.\venv\Scripts\Activate.ps1
```

### Error: "connection refused"

PostgreSQL isn't running. See Step 1 to start it.

---

## Quick Check Script

Run this to check your setup:

```powershell
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"
.\venv\Scripts\Activate.ps1

# Test database connection
python -c "from app.db.session import engine; from sqlalchemy import text; conn = engine.connect(); result = conn.execute(text('SELECT 1')); print('✅ Database connection: SUCCESS'); conn.close()"

# Check if tables exist
python -c "from app.db.session import engine; from sqlalchemy import inspect; inspector = inspect(engine); tables = inspector.get_table_names(); print(f'✅ Found {len(tables)} tables:', tables)"
```

If both commands succeed, your database is ready!

---

## Expected Result

After completing these steps:
- ✅ PostgreSQL running
- ✅ Database `interactive_novels` created
- ✅ All tables created (users, books, chapters, etc.)
- ✅ Backend server running with database connection
- ✅ Create Book feature works!

