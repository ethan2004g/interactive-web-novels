"""
Test script for Books API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_books_api():
    """Test the complete books management flow"""
    
    print("=" * 60)
    print("Testing Interactive Web Novels - Books API")
    print("=" * 60)
    
    # Step 1: Register and login as an author
    print("\n1. Setting up test author...")
    timestamp = str(int(time.time()))
    author_data = {
        "username": f"bookauthor{timestamp}",
        "email": f"bookauthor{timestamp}@example.com",
        "password": "AuthPass123",
        "role": "author"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=author_data)
        if response.status_code != 201:
            print(f"   [FAIL] Author registration failed: {response.json()}")
            return
        print("   [OK] Author registered successfully")
    except requests.exceptions.ConnectionError:
        print("   [FAIL] Cannot connect to server. Is it running?")
        print("   Hint: cd backend && run.bat")
        return
    
    # Login
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": author_data["username"], "password": author_data["password"]}
    )
    
    if login_response.status_code != 200:
        print(f"   [FAIL] Login failed: {login_response.json()}")
        return
    
    tokens = login_response.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    print(f"   [OK] Logged in as {author_data['username']}")
    
    # Step 2: Create a book
    print("\n2. Testing Create Book...")
    book_data = {
        "title": "The Chronicles of Interactive Fiction",
        "description": "An epic tale of code and creativity, where readers shape the story.",
        "genre": "Fantasy",
        "tags": ["interactive", "fantasy", "adventure"],
        "status": "ongoing"
    }
    
    response = requests.post(f"{BASE_URL}/books/", json=book_data, headers=headers)
    
    if response.status_code == 201:
        print("   [OK] Book created successfully!")
        book = response.json()
        book_id = book["id"]
        print(f"   Book ID: {book_id}")
        print(f"   Title: {book['title']}")
        print(f"   Status: {book['status']}")
        print(f"   Tags: {', '.join(book['tags'])}")
    else:
        print(f"   [FAIL] Book creation failed: {response.json()}")
        return
    
    # Step 3: Create another book
    print("\n3. Creating second book...")
    book_data_2 = {
        "title": "Mystery of the Missing Semicolon",
        "description": "A thrilling debugging adventure",
        "genre": "Mystery",
        "tags": ["mystery", "programming"],
        "status": "draft"
    }
    
    response = requests.post(f"{BASE_URL}/books/", json=book_data_2, headers=headers)
    if response.status_code == 201:
        print("   [OK] Second book created!")
        book2_id = response.json()["id"]
    else:
        print(f"   [FAIL] Second book creation failed")
        return
    
    # Step 4: Get all books
    print("\n4. Testing Get All Books...")
    response = requests.get(f"{BASE_URL}/books/")
    
    if response.status_code == 200:
        result = response.json()
        print("   [OK] Retrieved books list!")
        print(f"   Total books: {result['total']}")
        print(f"   Page: {result['page']}/{result['total_pages']}")
        print(f"   Books on this page: {len(result['books'])}")
    else:
        print(f"   [FAIL] Failed to get books: {response.json()}")
    
    # Step 5: Get my books
    print("\n5. Testing Get My Books...")
    response = requests.get(f"{BASE_URL}/books/my-books", headers=headers)
    
    if response.status_code == 200:
        my_books = response.json()
        print(f"   [OK] Retrieved {len(my_books)} of my books")
        for book in my_books:
            print(f"      - {book['title']} ({book['status']})")
    else:
        print(f"   [FAIL] Failed to get my books: {response.json()}")
    
    # Step 6: Get single book
    print("\n6. Testing Get Single Book...")
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    
    if response.status_code == 200:
        book = response.json()
        print("   [OK] Retrieved book details!")
        print(f"   Title: {book['title']}")
        print(f"   Views: {book['total_views']}")
        print(f"   Likes: {book['total_likes']}")
    else:
        print(f"   [FAIL] Failed to get book: {response.json()}")
    
    # Step 7: Update book
    print("\n7. Testing Update Book...")
    update_data = {
        "description": "UPDATED: An even more epic tale with plot twists!",
        "status": "completed"
    }
    
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        updated_book = response.json()
        print("   [OK] Book updated successfully!")
        print(f"   New description: {updated_book['description'][:50]}...")
        print(f"   New status: {updated_book['status']}")
    else:
        print(f"   [FAIL] Book update failed: {response.json()}")
    
    # Step 8: Search books
    print("\n8. Testing Search...")
    response = requests.get(f"{BASE_URL}/books/?search=Interactive")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] Search found {result['total']} book(s)")
        for book in result['books']:
            print(f"      - {book['title']}")
    else:
        print(f"   [FAIL] Search failed: {response.json()}")
    
    # Step 9: Filter by genre
    print("\n9. Testing Genre Filter...")
    response = requests.get(f"{BASE_URL}/books/?genre=Fantasy")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] Found {result['total']} Fantasy book(s)")
    else:
        print(f"   [FAIL] Genre filter failed: {response.json()}")
    
    # Step 10: Filter by tags
    print("\n10. Testing Tag Filter...")
    response = requests.get(f"{BASE_URL}/books/?tags=fantasy,adventure")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] Found {result['total']} book(s) with specified tags")
    else:
        print(f"   [FAIL] Tag filter failed: Status {response.status_code}")
        if response.text:
            print(f"   Error: {response.text[:200]}")
    
    # Step 11: Like a book
    print("\n11. Testing Like Book...")
    response = requests.post(f"{BASE_URL}/books/{book_id}/like", headers=headers)
    
    if response.status_code == 200:
        book = response.json()
        print(f"   [OK] Book liked! Total likes: {book['total_likes']}")
    else:
        print(f"   [FAIL] Like failed: {response.json()}")
    
    # Step 12: Test authorization (try to update someone else's book)
    print("\n12. Testing Authorization...")
    # Register another user
    reader_data = {
        "username": f"reader{timestamp}",
        "email": f"reader{timestamp}@example.com",
        "password": "ReaderPass123",
        "role": "reader"
    }
    requests.post(f"{BASE_URL}/auth/register", json=reader_data)
    reader_login = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": reader_data["username"], "password": reader_data["password"]}
    )
    reader_headers = {"Authorization": f"Bearer {reader_login.json()['access_token']}"}
    
    # Try to update the book
    response = requests.put(
        f"{BASE_URL}/books/{book_id}",
        json={"title": "Hacked!"},
        headers=reader_headers
    )
    
    if response.status_code == 403:
        print("   [OK] Authorization working! Reader cannot update author's book")
    elif response.status_code == 401:
        print("   [OK] Authorization working! Non-author cannot update book")
    else:
        print(f"   [FAIL] Authorization check failed: {response.status_code}")
    
    # Step 13: Delete second book
    print("\n13. Testing Delete Book...")
    response = requests.delete(f"{BASE_URL}/books/{book2_id}", headers=headers)
    
    if response.status_code == 204:
        print("   [OK] Book deleted successfully!")
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/books/{book2_id}")
        if response.status_code == 404:
            print("   [OK] Confirmed book is deleted")
        else:
            print("   [WARN] Book still exists after deletion")
    else:
        print(f"   [FAIL] Delete failed: {response.json()}")
    
    # Step 14: Pagination test
    print("\n14. Testing Pagination...")
    response = requests.get(f"{BASE_URL}/books/?page=1&page_size=5")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] Pagination working!")
        print(f"   Page {result['page']} of {result['total_pages']}")
        print(f"   Showing {len(result['books'])} of {result['total']} total books")
    else:
        print(f"   [FAIL] Pagination failed")
    
    print("\n" + "=" * 60)
    print("All Books API tests completed!")
    print("=" * 60)
    print("\nVisit http://localhost:8000/docs to explore the API interactively")
    print("=" * 60)


if __name__ == "__main__":
    test_books_api()

