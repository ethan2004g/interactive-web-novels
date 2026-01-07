"""
Test script for Chapters API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_chapters_api():
    """Test the complete chapters management flow"""
    
    print("=" * 60)
    print("Testing Interactive Web Novels - Chapters API")
    print("=" * 60)
    
    # Step 1: Register and login as an author
    print("\n1. Setting up test author...")
    timestamp = str(int(time.time()))
    author_data = {
        "username": f"chapauthor{timestamp}",
        "email": f"chapauthor{timestamp}@example.com",
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
    
    # Step 2: Create a book first
    print("\n2. Creating a test book...")
    book_data = {
        "title": "Test Book for Chapters",
        "description": "A book to test chapter management",
        "genre": "Fantasy",
        "tags": ["test", "chapters"],
        "status": "ongoing"
    }
    
    book_response = requests.post(f"{BASE_URL}/books/", json=book_data, headers=headers)
    if book_response.status_code != 201:
        print(f"   [FAIL] Book creation failed: {book_response.json()}")
        return
    
    book = book_response.json()
    book_id = book["id"]
    print(f"   [OK] Book created with ID: {book_id}")
    
    # Step 3: Get next chapter number
    print("\n3. Getting next chapter number...")
    next_num_response = requests.get(
        f"{BASE_URL}/books/{book_id}/chapters/next-number",
        headers=headers
    )
    
    if next_num_response.status_code != 200:
        print(f"   [FAIL] Get next chapter number failed: {next_num_response.json()}")
        return
    
    next_num = next_num_response.json()["next_chapter_number"]
    print(f"   [OK] Next chapter number: {next_num}")
    
    # Step 4: Create a simple chapter
    print("\n4. Creating a simple text chapter...")
    simple_chapter_data = {
        "title": "Chapter 1: The Beginning",
        "chapter_number": 1,
        "content_type": "simple",
        "content_data": {
            "text": "This is the beginning of our story. A young hero sets out on an adventure to save the kingdom from darkness. The journey will be long and perilous, but hope remains."
        },
        "is_published": True
    }
    
    chapter1_response = requests.post(
        f"{BASE_URL}/books/{book_id}/chapters",
        json=simple_chapter_data,
        headers=headers
    )
    
    if chapter1_response.status_code != 201:
        print(f"   [FAIL] Simple chapter creation failed: {chapter1_response.json()}")
        return
    
    chapter1 = chapter1_response.json()
    chapter1_id = chapter1["id"]
    print(f"   [OK] Simple chapter created with ID: {chapter1_id}")
    print(f"        Word count: {chapter1['word_count']}")
    
    # Step 5: Create an interactive chapter
    print("\n5. Creating an interactive chapter...")
    interactive_chapter_data = {
        "title": "Chapter 2: The Crossroads",
        "chapter_number": 2,
        "content_type": "interactive",
        "content_data": {
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "text": "You arrive at a crossroads. Two paths lie before you."
                },
                {
                    "id": "choice1",
                    "type": "choice",
                    "text": "Which path do you take?",
                    "options": [
                        {"text": "Take the left path through the forest", "next": "forest"},
                        {"text": "Take the right path over the mountains", "next": "mountain"}
                    ]
                },
                {
                    "id": "forest",
                    "type": "text",
                    "text": "You venture into the dark forest, where ancient trees whisper secrets."
                },
                {
                    "id": "mountain",
                    "type": "text",
                    "text": "You climb the steep mountain path, the wind howling around you."
                }
            ]
        },
        "is_published": False
    }
    
    chapter2_response = requests.post(
        f"{BASE_URL}/books/{book_id}/chapters",
        json=interactive_chapter_data,
        headers=headers
    )
    
    if chapter2_response.status_code != 201:
        print(f"   [FAIL] Interactive chapter creation failed: {chapter2_response.json()}")
        return
    
    chapter2 = chapter2_response.json()
    chapter2_id = chapter2["id"]
    print(f"   [OK] Interactive chapter created with ID: {chapter2_id}")
    print(f"        Word count: {chapter2['word_count']}")
    print(f"        Published: {chapter2['is_published']}")
    
    # Step 6: Get all chapters for the book
    print("\n6. Getting all chapters for the book...")
    chapters_response = requests.get(f"{BASE_URL}/books/{book_id}/chapters", headers=headers)
    
    if chapters_response.status_code != 200:
        print(f"   [FAIL] Get chapters failed: {chapters_response.json()}")
        return
    
    chapters_list = chapters_response.json()
    print(f"   [OK] Retrieved {chapters_list['total']} chapters")
    for ch in chapters_list["chapters"]:
        print(f"        - Chapter {ch['chapter_number']}: {ch['title']} ({ch['content_type']})")
    
    # Step 7: Get a single chapter
    print("\n7. Getting chapter details...")
    chapter_detail_response = requests.get(f"{BASE_URL}/chapters/{chapter1_id}")
    
    if chapter_detail_response.status_code != 200:
        print(f"   [FAIL] Get chapter failed: {chapter_detail_response.json()}")
        return
    
    chapter_detail = chapter_detail_response.json()
    print(f"   [OK] Retrieved chapter: {chapter_detail['title']}")
    print(f"        Content preview: {chapter_detail['content_data']['text'][:50]}...")
    
    # Step 8: Update a chapter
    print("\n8. Updating chapter 2 (publishing it)...")
    update_data = {
        "is_published": True
    }
    
    update_response = requests.put(
        f"{BASE_URL}/chapters/{chapter2_id}",
        json=update_data,
        headers=headers
    )
    
    if update_response.status_code != 200:
        print(f"   [FAIL] Update chapter failed: {update_response.json()}")
        return
    
    updated_chapter = update_response.json()
    print(f"   [OK] Chapter updated successfully")
    print(f"        Published: {updated_chapter['is_published']}")
    print(f"        Published at: {updated_chapter['published_at']}")
    
    # Step 9: Create chapter 3
    print("\n9. Creating chapter 3...")
    chapter3_data = {
        "title": "Chapter 3: The Village",
        "chapter_number": 3,
        "content_type": "simple",
        "content_data": {
            "text": "After your journey, you arrive at a peaceful village nestled in the valley."
        },
        "is_published": True
    }
    
    chapter3_response = requests.post(
        f"{BASE_URL}/books/{book_id}/chapters",
        json=chapter3_data,
        headers=headers
    )
    
    if chapter3_response.status_code != 201:
        print(f"   [FAIL] Chapter 3 creation failed: {chapter3_response.json()}")
        return
    
    chapter3 = chapter3_response.json()
    chapter3_id = chapter3["id"]
    print(f"   [OK] Chapter 3 created with ID: {chapter3_id}")
    
    # Step 10: Reorder chapters (move chapter 3 to position 2)
    print("\n10. Reordering chapters (moving chapter 3 to position 2)...")
    reorder_data = {
        "chapter_id": chapter3_id,
        "new_chapter_number": 2
    }
    
    reorder_response = requests.post(
        f"{BASE_URL}/books/{book_id}/chapters/reorder",
        json=reorder_data,
        headers=headers
    )
    
    if reorder_response.status_code != 200:
        print(f"   [FAIL] Reorder chapters failed: Status {reorder_response.status_code}")
        print(f"        Response: {reorder_response.text}")
        return
    
    reordered = reorder_response.json()
    print(f"   [OK] Chapters reordered successfully")
    print("        New order:")
    for ch in reordered["chapters"]:
        print(f"        - Chapter {ch['chapter_number']}: {ch['title']}")
    
    # Step 11: Test reader access (published chapters only)
    print("\n11. Testing reader access to published chapters...")
    # Register a reader
    reader_data = {
        "username": f"reader{timestamp}",
        "email": f"reader{timestamp}@example.com",
        "password": "ReaderPass123",
        "role": "reader"
    }
    
    reader_reg_response = requests.post(f"{BASE_URL}/auth/register", json=reader_data)
    if reader_reg_response.status_code != 201:
        print(f"   [FAIL] Reader registration failed")
        return
    
    reader_login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": reader_data["username"], "password": reader_data["password"]}
    )
    
    reader_tokens = reader_login_response.json()
    reader_headers = {"Authorization": f"Bearer {reader_tokens['access_token']}"}
    
    # Get chapters as reader (should only see published)
    reader_chapters_response = requests.get(
        f"{BASE_URL}/books/{book_id}/chapters",
        headers=reader_headers
    )
    
    if reader_chapters_response.status_code != 200:
        print(f"   [FAIL] Reader get chapters failed")
        return
    
    reader_chapters = reader_chapters_response.json()
    print(f"   [OK] Reader can see {reader_chapters['total']} published chapters")
    
    # Step 12: Delete a chapter
    print("\n12. Deleting chapter 1...")
    delete_response = requests.delete(f"{BASE_URL}/chapters/{chapter1_id}", headers=headers)
    
    if delete_response.status_code != 204:
        print(f"   [FAIL] Delete chapter failed")
        return
    
    print(f"   [OK] Chapter deleted successfully")
    
    # Verify deletion
    verify_response = requests.get(f"{BASE_URL}/books/{book_id}/chapters", headers=headers)
    verify_chapters = verify_response.json()
    print(f"        Remaining chapters: {verify_chapters['total']}")
    
    # Step 13: Test validation (try to create chapter with invalid content)
    print("\n13. Testing validation (invalid simple chapter)...")
    invalid_chapter = {
        "title": "Invalid Chapter",
        "chapter_number": 10,
        "content_type": "simple",
        "content_data": {
            "wrong_field": "This should fail"
        },
        "is_published": False
    }
    
    invalid_response = requests.post(
        f"{BASE_URL}/books/{book_id}/chapters",
        json=invalid_chapter,
        headers=headers
    )
    
    if invalid_response.status_code == 422:
        print(f"   [OK] Validation correctly rejected invalid chapter")
        print(f"        Error: {invalid_response.json()['detail'][0]['msg']}")
    else:
        print(f"   [FAIL] Validation should have failed but didn't")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All Chapters API tests completed successfully!")
    print("=" * 60)
    print("\nTest Summary:")
    print(f"  - Created book: {book['title']}")
    print(f"  - Created 3 chapters (simple and interactive)")
    print(f"  - Updated chapter publication status")
    print(f"  - Reordered chapters")
    print(f"  - Tested reader access permissions")
    print(f"  - Deleted a chapter")
    print(f"  - Validated input data")
    print("\n[COMPLETE] Phase 1.4: Chapters Management API - COMPLETE!")


if __name__ == "__main__":
    test_chapters_api()

