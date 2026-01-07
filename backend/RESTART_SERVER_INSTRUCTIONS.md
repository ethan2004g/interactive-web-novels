# Server Restart Instructions

## Why Restart?

After implementing Phase 1.6 (File Upload & Storage), the FastAPI server needs to be **manually restarted** for the new file upload routes to become available. The auto-reload feature may not always pick up new router registrations.

## How to Restart

### Step 1: Stop the Current Server

In the terminal where the server is running, press:
```
Ctrl + C
```

Wait for the server to shut down completely.

### Step 2: Restart the Server

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

Or use the run script:
```bash
cd backend
.\run.ps1
```

### Step 3: Verify Server is Running

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Testing File Upload

After restarting, run the test script:

```bash
cd backend
.\venv\Scripts\python.exe test_file_uploads.py
```

Expected output:
```
============================================================
INTERACTIVE WEB NOVELS - FILE UPLOAD TEST SUITE
============================================================

[OK] User registered successfully
[OK] Login successful
[OK] Book created successfully
[OK] Upload info retrieved
[OK] Cover image uploaded
[OK] Book updated with cover image
[OK] Cover image is accessible
[OK] Thumbnail is accessible
[OK] Chapter image uploaded
...
```

## Verify Routes are Available

Test the upload info endpoint:
```bash
curl http://localhost:8000/api/v1/files/info
```

Expected response:
```json
{
  "max_file_size_mb": 10.0,
  "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
  "thumbnail_size": [300, 400]
}
```

## Common Issues

### Issue: Routes still return 404
**Solution:** Make sure you completely stopped the old server process before restarting.

### Issue: "Directory not found" error
**Solution:** The `uploads/` directory should be created automatically. If not, create it manually:
```bash
mkdir -p uploads/images/covers
mkdir -p uploads/images/chapters
mkdir -p uploads/images/thumbnails
```

### Issue: Permission denied when saving files
**Solution:** Check that the `uploads/` directory has write permissions.

## Next Steps

Once the server is restarted and file uploads are working:
1. Test the file upload endpoints with the test script
2. Try uploading images through the API
3. Verify images are accessible via the `/uploads/` URL path
4. Proceed to Phase 1.7 or Phase 2

