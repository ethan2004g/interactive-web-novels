#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to verify backend is running and can accept book creation
"""
import requests
import json
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000/api/v1"

def test_backend_connection():
    """Test if backend is responding"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_register_and_create_book():
    """Test full flow: register, login, create book"""
    
    # 1. Register a test user
    print("\n1. Registering test user...")
    register_data = {
        "username": "testauthor123",
        "email": "testauthor123@test.com",
        "password": "testpass123",
        "role": "author"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            print("✅ User registered successfully")
        elif response.status_code == 400 and "already registered" in response.text:
            print("ℹ️  User already exists, continuing...")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "username": "testauthor123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print("✅ Login successful")
            print(f"   Token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # 3. Create a book
    print("\n3. Creating a test book...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    book_data = {
        "title": "Test Book from API",
        "description": "This is a test book created via the API to verify the connection",
        "genre": "Fantasy",
        "tags": ["test", "api"],
        "status": "draft"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/books", json=book_data, headers=headers)
        if response.status_code in [200, 201]:
            book = response.json()
            print("✅ Book created successfully!")
            print(f"   Book ID: {book.get('id')}")
            print(f"   Title: {book.get('title')}")
            print(f"   Status: {book.get('status')}")
            return True
        else:
            print(f"❌ Book creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Book creation error: {e}")
        return False

def check_books_in_database():
    """Check if books exist in database"""
    print("\n4. Checking books in database...")
    try:
        response = requests.get(f"{BASE_URL}/books?size=5")
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            books = data.get('items', [])
            print(f"✅ Found {total} book(s) in database")
            for book in books[:3]:  # Show first 3
                print(f"   - {book.get('title')} by user #{book.get('author_id')}")
            return True
        else:
            print(f"❌ Failed to fetch books: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error fetching books: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Backend Connection Test")
    print("=" * 60)
    
    # Test 1: Basic connection
    if not test_backend_connection():
        print("\n❌ Backend is not running!")
        print("   Start it with: uvicorn main:app --reload")
        exit(1)
    
    # Test 2: Full flow
    if test_register_and_create_book():
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Backend is working correctly")
        print("=" * 60)
        
        # Test 3: Verify data persisted
        check_books_in_database()
        
        print("\n📝 Next steps:")
        print("   1. Check if you can see the book in the frontend")
        print("   2. Try creating a book from the UI")
        print("   3. Check browser console for any errors")
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED! There's an issue with the backend")
        print("=" * 60)
        print("\n🔍 Troubleshooting:")
        print("   1. Check backend logs for errors")
        print("   2. Verify database connection in .env file")
        print("   3. Make sure PostgreSQL is running")

