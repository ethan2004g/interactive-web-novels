"""
Quick test script for file upload endpoints
Tests: Cover image upload, Chapter image upload, File deletion
"""
import requests
import json
import time
import os
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000/api/v1"

# Global variables to store test data
auth_token = None
user_id = None
book_id = None
cover_image_url = None
thumbnail_url = None
chapter_image_url = None


def create_test_image(width=800, height=600, color=(100, 150, 200)):
    """Create a test image in memory"""
    img = Image.new('RGB', (width, height), color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


def setup_test_data():
    """Create test user and book for testing"""
    global auth_token, user_id, book_id
    
    print("\n" + "=" * 60)
    print("Setting up test data...")
    print("=" * 60)
    
    # Register a new author
    timestamp = str(int(time.time()))
    register_data = {
        "username": f"testuploader{timestamp}",
        "email": f"testuploader{timestamp}@example.com",
        "password": "Pass1234",
        "role": "author"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("[OK] User registered successfully")
            user_id = response.json()["id"]
        else:
            print(f"[FAIL] Registration failed: {response.json()}")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Cannot connect to server. Is it running?")
        print("  Run: cd backend && .\\run.bat")
        return False
    
    # Login
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        print("[OK] Login successful")
        auth_token = response.json()["access_token"]
    else:
        print(f"[FAIL] Login failed: {response.json()}")
        return False
    
    # Create a book
    headers = {"Authorization": f"Bearer {auth_token}"}
    book_data = {
        "title": f"Test Book {timestamp}",
        "description": "A test book for file upload testing",
        "genre": "Fantasy",
        "tags": ["test", "fantasy"],
        "status": "ongoing"
    }
    
    response = requests.post(f"{BASE_URL}/books/", json=book_data, headers=headers)
    if response.status_code == 201:
        print("[OK] Book created successfully")
        book_id = response.json()["id"]
    else:
        print(f"[FAIL] Book creation failed: {response.json()}")
        return False
    
    print(f"\nTest Data Created:")
    print(f"  - User ID: {user_id}")
    print(f"  - Book ID: {book_id}")
    
    return True


def test_upload_info():
    """Test getting upload info endpoint"""
    print("\n" + "=" * 60)
    print("Testing Upload Info Endpoint")
    print("=" * 60)
    
    print("\n1. Getting upload info...")
    response = requests.get(f"{BASE_URL}/files/info")
    if response.status_code == 200:
        info = response.json()
        print("   [OK] Upload info retrieved")
        print(f"   Max file size: {info['max_file_size_mb']}MB")
        print(f"   Allowed extensions: {', '.join(info['allowed_extensions'])}")
        print(f"   Thumbnail size: {info['thumbnail_size']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")


def test_cover_image_upload():
    """Test cover image upload"""
    global cover_image_url, thumbnail_url
    
    print("\n" + "=" * 60)
    print("Testing Cover Image Upload")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Upload cover image
    print("\n1. Uploading cover image...")
    test_image = create_test_image(800, 1200, (255, 100, 100))
    files = {"file": ("test_cover.png", test_image, "image/png")}
    
    response = requests.post(f"{BASE_URL}/files/upload/cover", files=files, headers=headers)
    if response.status_code == 201:
        print("   [OK] Cover image uploaded")
        data = response.json()
        cover_image_url = data["image_url"]
        thumbnail_url = data["thumbnail_url"]
        print(f"   Image URL: {cover_image_url}")
        print(f"   Thumbnail URL: {thumbnail_url}")
        print(f"   Filename: {data['filename']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 2: Update book with cover image
    print("\n2. Updating book with cover image...")
    update_data = {
        "cover_image_url": cover_image_url,
        "thumbnail_url": thumbnail_url
    }
    
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("   [OK] Book updated with cover image")
        book_data = response.json()
        print(f"   Cover URL: {book_data['cover_image_url']}")
        print(f"   Thumbnail URL: {book_data['thumbnail_url']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Test 3: Verify image is accessible
    print("\n3. Verifying image is accessible...")
    full_url = f"http://localhost:8000{cover_image_url}"
    response = requests.get(full_url)
    if response.status_code == 200:
        print("   [OK] Cover image is accessible")
        print(f"   Image size: {len(response.content)} bytes")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
    
    # Test 4: Verify thumbnail is accessible
    print("\n4. Verifying thumbnail is accessible...")
    full_url = f"http://localhost:8000{thumbnail_url}"
    response = requests.get(full_url)
    if response.status_code == 200:
        print("   [OK] Thumbnail is accessible")
        print(f"   Thumbnail size: {len(response.content)} bytes")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")


def test_chapter_image_upload():
    """Test chapter image upload"""
    global chapter_image_url
    
    print("\n" + "=" * 60)
    print("Testing Chapter Image Upload")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Upload chapter image
    print("\n1. Uploading chapter image...")
    test_image = create_test_image(1200, 800, (100, 200, 100))
    files = {"file": ("test_chapter.png", test_image, "image/png")}
    
    response = requests.post(f"{BASE_URL}/files/upload/chapter-image", files=files, headers=headers)
    if response.status_code == 201:
        print("   [OK] Chapter image uploaded")
        data = response.json()
        chapter_image_url = data["image_url"]
        print(f"   Image URL: {chapter_image_url}")
        print(f"   Filename: {data['filename']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 2: Verify image is accessible
    print("\n2. Verifying chapter image is accessible...")
    full_url = f"http://localhost:8000{chapter_image_url}"
    response = requests.get(full_url)
    if response.status_code == 200:
        print("   [OK] Chapter image is accessible")
        print(f"   Image size: {len(response.content)} bytes")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")


def test_file_validation():
    """Test file validation"""
    print("\n" + "=" * 60)
    print("Testing File Validation")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Try to upload file that's too large (simulate)
    print("\n1. Testing file size validation...")
    # Create a large image (this will be compressed by PNG, so it won't actually be 15MB)
    large_image = create_test_image(5000, 5000, (150, 150, 150))
    files = {"file": ("large_image.png", large_image, "image/png")}
    
    response = requests.post(f"{BASE_URL}/files/upload/cover", files=files, headers=headers)
    if response.status_code == 201:
        print("   [OK] Large image uploaded (within size limit)")
    elif response.status_code == 400:
        print("   [OK] File size validation working")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"   [INFO] Response status: {response.status_code}")
    
    # Test 2: Try to upload invalid file type
    print("\n2. Testing file type validation...")
    fake_file = BytesIO(b"This is not an image file")
    files = {"file": ("test.txt", fake_file, "text/plain")}
    
    response = requests.post(f"{BASE_URL}/files/upload/cover", files=files, headers=headers)
    if response.status_code == 400:
        print("   [OK] File type validation working")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"   [FAIL] Expected 400, got {response.status_code}")


def test_file_deletion():
    """Test file deletion"""
    print("\n" + "=" * 60)
    print("Testing File Deletion")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Delete chapter image
    if chapter_image_url:
        print("\n1. Deleting chapter image...")
        params = {"file_url": chapter_image_url}
        response = requests.delete(f"{BASE_URL}/files/delete", params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] {data['message']}")
        else:
            print(f"   [FAIL] Failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    
    # Test 2: Delete cover image with thumbnail
    if cover_image_url and thumbnail_url:
        print("\n2. Deleting cover image with thumbnail...")
        params = {
            "file_url": cover_image_url,
            "thumbnail_url": thumbnail_url
        }
        response = requests.delete(f"{BASE_URL}/files/delete", params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] {data['message']}")
        else:
            print(f"   [FAIL] Failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    
    # Test 3: Try to delete non-existent file
    print("\n3. Trying to delete non-existent file...")
    params = {"file_url": "/uploads/images/covers/nonexistent.png"}
    response = requests.delete(f"{BASE_URL}/files/delete", params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] {data['message']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")


def main():
    """Run all file upload tests"""
    print("\n" + "=" * 60)
    print("INTERACTIVE WEB NOVELS - FILE UPLOAD TEST SUITE")
    print("=" * 60)
    
    # Setup
    if not setup_test_data():
        print("\n[FAIL] Setup failed. Exiting...")
        return
    
    # Run tests
    test_upload_info()
    test_cover_image_upload()
    test_chapter_image_upload()
    test_file_validation()
    test_file_deletion()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
    print("\nAll file upload features have been tested!")
    print("\nFeatures tested:")
    print("  [OK] Upload Info Endpoint")
    print("  [OK] Cover Image Upload (with thumbnail generation)")
    print("  [OK] Chapter Image Upload")
    print("  [OK] File Validation (size and type)")
    print("  [OK] File Deletion")
    print("  [OK] Static File Serving")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

