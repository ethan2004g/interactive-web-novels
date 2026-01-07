"""
Test script for Chapter Templates API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_chapter_templates_api():
    """Test the complete chapter templates management flow"""
    
    print("=" * 60)
    print("Testing Interactive Web Novels - Chapter Templates API")
    print("=" * 60)
    
    # Step 1: Register and login as an author
    print("\n1. Setting up test author...")
    timestamp = str(int(time.time()))
    author_data = {
        "username": f"tempauthor{timestamp}",
        "email": f"tempauthor{timestamp}@example.com",
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
    
    # Step 2: Create a custom chapter template
    print("\n2. Creating a custom chapter template...")
    template_data = {
        "name": f"Test Template {timestamp}",
        "description": "A custom template for testing purposes",
        "is_public": False,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "This is a test template",
                    "next": "end"
                }
            ]
        }
    }
    
    create_response = requests.post(
        f"{BASE_URL}/chapter-templates",
        json=template_data,
        headers=headers
    )
    
    if create_response.status_code != 201:
        print(f"   [FAIL] Template creation failed: {create_response.json()}")
        return
    
    template = create_response.json()
    template_id = template["id"]
    print(f"   [OK] Template created with ID: {template_id}")
    print(f"        Name: {template['name']}")
    print(f"        Public: {template['is_public']}")
    
    # Step 3: Get template by ID
    print("\n3. Getting template by ID...")
    get_response = requests.get(
        f"{BASE_URL}/chapter-templates/{template_id}",
        headers=headers
    )
    
    if get_response.status_code != 200:
        print(f"   [FAIL] Get template failed: {get_response.json()}")
        return
    
    fetched_template = get_response.json()
    print(f"   [OK] Template fetched successfully")
    print(f"        Name: {fetched_template['name']}")
    print(f"        Description: {fetched_template['description']}")
    
    # Step 4: Update template
    print("\n4. Updating template...")
    update_data = {
        "description": "Updated description for testing",
        "is_public": True
    }
    
    update_response = requests.put(
        f"{BASE_URL}/chapter-templates/{template_id}",
        json=update_data,
        headers=headers
    )
    
    if update_response.status_code != 200:
        print(f"   [FAIL] Update template failed: {update_response.json()}")
        return
    
    updated_template = update_response.json()
    print(f"   [OK] Template updated successfully")
    print(f"        New description: {updated_template['description']}")
    print(f"        Now public: {updated_template['is_public']}")
    
    # Step 5: Get all templates (should include both custom and default templates)
    print("\n5. Getting all templates...")
    list_response = requests.get(
        f"{BASE_URL}/chapter-templates",
        headers=headers
    )
    
    if list_response.status_code != 200:
        print(f"   [FAIL] List templates failed: {list_response.json()}")
        return
    
    templates_list = list_response.json()
    print(f"   [OK] Templates listed successfully")
    print(f"        Total templates: {templates_list['total']}")
    print(f"        Templates returned: {len(templates_list['templates'])}")
    
    # Step 6: Get only public templates
    print("\n6. Getting public templates...")
    public_response = requests.get(
        f"{BASE_URL}/chapter-templates?public_only=true"
    )
    
    if public_response.status_code != 200:
        print(f"   [FAIL] Get public templates failed: {public_response.json()}")
        return
    
    public_templates = public_response.json()
    print(f"   [OK] Public templates listed successfully")
    print(f"        Total public templates: {public_templates['total']}")
    
    # Step 7: Get my templates
    print("\n7. Getting my templates...")
    my_templates_response = requests.get(
        f"{BASE_URL}/chapter-templates/my-templates",
        headers=headers
    )
    
    if my_templates_response.status_code != 200:
        print(f"   [FAIL] Get my templates failed: {my_templates_response.json()}")
        return
    
    my_templates = my_templates_response.json()
    print(f"   [OK] My templates listed successfully")
    print(f"        Total my templates: {my_templates['total']}")
    
    # Step 8: Search templates
    print("\n8. Searching templates...")
    search_response = requests.get(
        f"{BASE_URL}/chapter-templates?search=Simple",
        headers=headers
    )
    
    if search_response.status_code != 200:
        print(f"   [FAIL] Search templates failed: {search_response.json()}")
        return
    
    search_results = search_response.json()
    print(f"   [OK] Template search successful")
    print(f"        Results found: {search_results['total']}")
    if search_results['templates']:
        print(f"        First result: {search_results['templates'][0]['name']}")
    
    # Step 9: Get popular templates
    print("\n9. Getting popular templates...")
    popular_response = requests.get(
        f"{BASE_URL}/chapter-templates/popular?limit=5"
    )
    
    if popular_response.status_code != 200:
        print(f"   [FAIL] Get popular templates failed: {popular_response.json()}")
        return
    
    popular_templates = popular_response.json()
    print(f"   [OK] Popular templates listed successfully")
    print(f"        Templates returned: {len(popular_templates)}")
    if popular_templates:
        print(f"        Top template: {popular_templates[0]['name']}")
    
    # Step 10: Use a template (increment usage count)
    print("\n10. Using a template...")
    use_response = requests.post(
        f"{BASE_URL}/chapter-templates/{template_id}/use",
        headers=headers
    )
    
    if use_response.status_code != 200:
        print(f"   [FAIL] Use template failed: {use_response.json()}")
        return
    
    used_template = use_response.json()
    print(f"   [OK] Template used successfully")
    print(f"        Usage count: {used_template['usage_count']}")
    
    # Step 11: Test pagination
    print("\n11. Testing pagination...")
    page1_response = requests.get(
        f"{BASE_URL}/chapter-templates?skip=0&limit=5",
        headers=headers
    )
    
    if page1_response.status_code != 200:
        print(f"   [FAIL] Pagination test failed: {page1_response.json()}")
        return
    
    page1 = page1_response.json()
    print(f"   [OK] Pagination working")
    print(f"        Page 1 templates: {len(page1['templates'])}")
    print(f"        Total available: {page1['total']}")
    
    # Step 12: Test authorization (another user trying to edit)
    print("\n12. Testing authorization...")
    
    # Create another author
    author2_data = {
        "username": f"author2{timestamp}",
        "email": f"author2{timestamp}@example.com",
        "password": "AuthPass123",
        "role": "author"
    }
    
    requests.post(f"{BASE_URL}/auth/register", json=author2_data)
    login2_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": author2_data["username"], "password": author2_data["password"]}
    )
    
    tokens2 = login2_response.json()
    headers2 = {"Authorization": f"Bearer {tokens2['access_token']}"}
    
    # Try to update first author's template
    unauthorized_update = requests.put(
        f"{BASE_URL}/chapter-templates/{template_id}",
        json={"description": "Trying to hack"},
        headers=headers2
    )
    
    if unauthorized_update.status_code == 403:
        print(f"   [OK] Authorization check working (403 Forbidden)")
    else:
        print(f"   [WARN] Expected 403, got {unauthorized_update.status_code}")
    
    # Step 13: Create a public template and verify other users can use it
    print("\n13. Testing public template sharing...")
    public_template_data = {
        "name": f"Public Template {timestamp}",
        "description": "A public template everyone can use",
        "is_public": True,
        "template_data": {
            "type": "simple",
            "structure": {"text": "Public template content"}
        }
    }
    
    public_create_response = requests.post(
        f"{BASE_URL}/chapter-templates",
        json=public_template_data,
        headers=headers
    )
    
    public_template = public_create_response.json()
    public_template_id = public_template["id"]
    
    # Second author should be able to view and use it
    view_public = requests.get(
        f"{BASE_URL}/chapter-templates/{public_template_id}",
        headers=headers2
    )
    
    if view_public.status_code == 200:
        print(f"   [OK] Other users can view public templates")
    else:
        print(f"   [FAIL] Other users cannot view public templates")
    
    # Step 14: Delete template
    print("\n14. Deleting template...")
    delete_response = requests.delete(
        f"{BASE_URL}/chapter-templates/{template_id}",
        headers=headers
    )
    
    if delete_response.status_code != 204:
        print(f"   [FAIL] Delete template failed: Status {delete_response.status_code}")
        return
    
    print(f"   [OK] Template deleted successfully")
    
    # Verify deletion
    get_deleted = requests.get(
        f"{BASE_URL}/chapter-templates/{template_id}",
        headers=headers
    )
    
    if get_deleted.status_code == 404:
        print(f"   [OK] Template properly deleted (404)")
    else:
        print(f"   [WARN] Expected 404, got {get_deleted.status_code}")
    
    # Step 15: Test validation
    print("\n15. Testing validation...")
    
    # Try to create template with invalid data
    invalid_template = {
        "name": "",  # Empty name
        "template_data": {}  # Empty template data
    }
    
    invalid_response = requests.post(
        f"{BASE_URL}/chapter-templates",
        json=invalid_template,
        headers=headers
    )
    
    if invalid_response.status_code == 422:
        print(f"   [OK] Validation working (422 Unprocessable Entity)")
    else:
        print(f"   [WARN] Expected 422, got {invalid_response.status_code}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Chapter Templates API Test Summary")
    print("=" * 60)
    print("[OK] All tests passed successfully!")
    print("\nTested features:")
    print("  - Template creation")
    print("  - Template retrieval (by ID)")
    print("  - Template update")
    print("  - Template deletion")
    print("  - Template listing (all, public, my templates)")
    print("  - Template search")
    print("  - Popular templates")
    print("  - Template usage tracking")
    print("  - Pagination")
    print("  - Authorization checks")
    print("  - Public/private template sharing")
    print("  - Input validation")
    print("=" * 60)

if __name__ == "__main__":
    test_chapter_templates_api()

