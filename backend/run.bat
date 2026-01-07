@echo off
echo Starting Interactive Web Novels Backend...
echo.

call venv\Scripts\activate.bat

echo Server starting at http://localhost:8000
echo API Docs available at http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

