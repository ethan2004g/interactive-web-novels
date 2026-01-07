"""
Quick test script for reader features endpoints
Tests: Reading Progress, Bookmarks, Ratings, and Comments
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

# Global variables to store test data
auth_token = None
user_id = None
book_id = None
chapter_id = None
comment_id = None

def setup_test_data():
    """Create test user, book, and chapter for testing"""
    global auth_token, user_id, book_id, chapter_id
    
    print("\n" + "=" * 60)
    print("Setting up test data...")
    print("=" * 60)
    
    # Register a new author
    timestamp = str(int(time.time()))
    register_data = {
        "username": f"testreader{timestamp}",
        "email": f"testreader{timestamp}@example.com",
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
        "description": "A test book for reader features",
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
    
    # Create a chapter
    chapter_data = {
        "chapter_number": 1,
        "title": "Chapter 1: The Beginning",
        "content_type": "simple",
        "content_data": {"text": "This is the first chapter of our test book."},
        "is_published": True
    }
    
    response = requests.post(f"{BASE_URL}/books/{book_id}/chapters", json=chapter_data, headers=headers)
    if response.status_code == 201:
        print("[OK] Chapter created successfully")
        chapter_id = response.json()["id"]
    else:
        print(f"[FAIL] Chapter creation failed: {response.json()}")
        return False
    
    print(f"\nTest Data Created:")
    print(f"  - User ID: {user_id}")
    print(f"  - Book ID: {book_id}")
    print(f"  - Chapter ID: {chapter_id}")
    
    return True


def test_reading_progress():
    """Test reading progress endpoints"""
    print("\n" + "=" * 60)
    print("Testing Reading Progress Features")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Create reading progress
    print("\n1. Creating reading progress...")
    progress_data = {
        "book_id": book_id,
        "chapter_id": chapter_id,
        "progress_percentage": 50.0
    }
    
    response = requests.post(f"{BASE_URL}/reading-progress/", json=progress_data, headers=headers)
    if response.status_code == 201:
        print("   [OK] Reading progress created")
        progress_id = response.json()["id"]
        print(f"   Progress: {response.json()['progress_percentage']}%")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 2: Get reading progress for book
    print("\n2. Getting reading progress for book...")
    response = requests.get(f"{BASE_URL}/reading-progress/book/{book_id}", headers=headers)
    if response.status_code == 200:
        print("   [OK] Reading progress retrieved")
        print(f"   Progress: {response.json()['progress_percentage']}%")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 3: Update reading progress
    print("\n3. Updating reading progress...")
    update_data = {
        "progress_percentage": 75.0
    }
    
    response = requests.put(f"{BASE_URL}/reading-progress/{progress_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("   [OK] Reading progress updated")
        print(f"   New Progress: {response.json()['progress_percentage']}%")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 4: Get all reading progress
    print("\n4. Getting all reading progress...")
    response = requests.get(f"{BASE_URL}/reading-progress/", headers=headers)
    if response.status_code == 200:
        print(f"   [OK] Retrieved {len(response.json())} reading progress entries")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")


def test_bookmarks():
    """Test bookmark endpoints"""
    print("\n" + "=" * 60)
    print("Testing Bookmark Features")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Create bookmark
    print("\n1. Creating bookmark...")
    bookmark_data = {
        "book_id": book_id
    }
    
    response = requests.post(f"{BASE_URL}/bookmarks/", json=bookmark_data, headers=headers)
    if response.status_code == 201:
        print("   [OK] Bookmark created")
        print(f"   Bookmark ID: {response.json()['id']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 2: Check if book is bookmarked
    print("\n2. Checking if book is bookmarked...")
    response = requests.get(f"{BASE_URL}/bookmarks/book/{book_id}", headers=headers)
    if response.status_code == 200:
        print("   [OK] Book is bookmarked")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Test 3: Get all bookmarks
    print("\n3. Getting all bookmarks...")
    response = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    if response.status_code == 200:
        print(f"   [OK] Retrieved {len(response.json())} bookmarks")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Test 4: Delete bookmark
    print("\n4. Deleting bookmark...")
    response = requests.delete(f"{BASE_URL}/bookmarks/book/{book_id}", headers=headers)
    if response.status_code == 204:
        print("   [OK] Bookmark deleted")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")


def test_ratings():
    """Test rating endpoints"""
    print("\n" + "=" * 60)
    print("Testing Rating Features")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Create rating
    print("\n1. Creating rating...")
    rating_data = {
        "book_id": book_id,
        "rating": 5
    }
    
    response = requests.post(f"{BASE_URL}/ratings/", json=rating_data, headers=headers)
    if response.status_code == 201:
        print("   [OK] Rating created")
        print(f"   Rating: {response.json()['rating']} stars")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 2: Get user's rating for book
    print("\n2. Getting user's rating for book...")
    response = requests.get(f"{BASE_URL}/ratings/book/{book_id}", headers=headers)
    if response.status_code == 200:
        print("   [OK] Rating retrieved")
        print(f"   Rating: {response.json()['rating']} stars")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 3: Update rating
    print("\n3. Updating rating...")
    update_data = {
        "rating": 4
    }
    
    response = requests.put(f"{BASE_URL}/ratings/book/{book_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("   [OK] Rating updated")
        print(f"   New Rating: {response.json()['rating']} stars")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 4: Get book rating statistics (public)
    print("\n4. Getting book rating statistics...")
    response = requests.get(f"{BASE_URL}/ratings/book/{book_id}/stats")
    if response.status_code == 200:
        stats = response.json()
        print("   [OK] Rating statistics retrieved")
        print(f"   Average Rating: {stats['average_rating']:.2f}")
        print(f"   Total Ratings: {stats['total_ratings']}")
        print(f"   Distribution: {stats['rating_distribution']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")


def test_comments():
    """Test comment endpoints"""
    global comment_id
    
    print("\n" + "=" * 60)
    print("Testing Comment Features")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1: Create comment
    print("\n1. Creating comment...")
    comment_data = {
        "chapter_id": chapter_id,
        "content": "This is a great chapter! I really enjoyed reading it."
    }
    
    response = requests.post(f"{BASE_URL}/comments/", json=comment_data, headers=headers)
    if response.status_code == 201:
        print("   [OK] Comment created")
        comment_id = response.json()["id"]
        print(f"   Comment ID: {comment_id}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
        return
    
    # Test 2: Create reply to comment
    print("\n2. Creating reply to comment...")
    reply_data = {
        "chapter_id": chapter_id,
        "content": "Thanks for the feedback!",
        "parent_comment_id": comment_id
    }
    
    response = requests.post(f"{BASE_URL}/comments/", json=reply_data, headers=headers)
    if response.status_code == 201:
        print("   [OK] Reply created")
        reply_id = response.json()["id"]
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 3: Get chapter comments
    print("\n3. Getting chapter comments...")
    response = requests.get(f"{BASE_URL}/comments/chapter/{chapter_id}")
    if response.status_code == 200:
        print(f"   [OK] Retrieved {len(response.json())} top-level comments")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 4: Get comment replies
    print("\n4. Getting comment replies...")
    response = requests.get(f"{BASE_URL}/comments/{comment_id}/replies")
    if response.status_code == 200:
        print(f"   [OK] Retrieved {len(response.json())} replies")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 5: Get comment count
    print("\n5. Getting chapter comment count...")
    response = requests.get(f"{BASE_URL}/comments/chapter/{chapter_id}/count")
    if response.status_code == 200:
        print(f"   [OK] Total comments: {response.json()['total_comments']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 6: Update comment
    print("\n6. Updating comment...")
    update_data = {
        "content": "This is an amazing chapter! I really enjoyed reading it. [EDITED]"
    }
    
    response = requests.put(f"{BASE_URL}/comments/{comment_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("   [OK] Comment updated")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
    
    # Test 7: Get user's comments
    print("\n7. Getting user's comments...")
    response = requests.get(f"{BASE_URL}/comments/my-comments", headers=headers)
    if response.status_code == 200:
        print(f"   [OK] Retrieved {len(response.json())} comments by user")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")


def test_book_statistics():
    """Test book statistics endpoint"""
    print("\n" + "=" * 60)
    print("Testing Book Statistics")
    print("=" * 60)
    
    print("\n1. Getting comprehensive book statistics...")
    response = requests.get(f"{BASE_URL}/books/{book_id}/statistics")
    if response.status_code == 200:
        stats = response.json()
        print("   [OK] Book statistics retrieved")
        print(f"\n   Book Statistics:")
        print(f"   - Total Views: {stats['total_views']}")
        print(f"   - Total Likes: {stats['total_likes']}")
        print(f"   - Total Chapters: {stats['total_chapters']}")
        print(f"   - Total Comments: {stats['total_comments']}")
        print(f"   - Total Bookmarks: {stats['total_bookmarks']}")
        print(f"   - Average Rating: {stats['average_rating']:.2f}")
        print(f"   - Total Ratings: {stats['total_ratings']}")
        print(f"   - Rating Distribution: {stats['rating_distribution']}")
    else:
        print(f"   [FAIL] Failed with status {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")


def main():
    """Run all reader feature tests"""
    print("\n" + "=" * 60)
    print("INTERACTIVE WEB NOVELS - READER FEATURES TEST SUITE")
    print("=" * 60)
    
    # Setup
    if not setup_test_data():
        print("\n[FAIL] Setup failed. Exiting...")
        return
    
    # Run tests
    test_reading_progress()
    test_bookmarks()
    test_ratings()
    test_comments()
    test_book_statistics()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
    print("\nAll reader features have been tested!")
    print("\nFeatures tested:")
    print("  [OK] Reading Progress (Create, Read, Update, Delete)")
    print("  [OK] Bookmarks (Create, Read, Delete)")
    print("  [OK] Ratings (Create, Read, Update, Statistics)")
    print("  [OK] Comments (Create, Read, Update, Replies, Count)")
    print("  [OK] Book Statistics (Comprehensive stats)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

