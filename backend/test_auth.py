"""
Quick test script for authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_authentication_flow():
    """Test the complete authentication flow"""
    
    print("=" * 60)
    print("Testing Interactive Web Novels Authentication System")
    print("=" * 60)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    import time
    timestamp = str(int(time.time()))
    register_data = {
        "username": f"testauthor{timestamp}",
        "email": f"testauthor{timestamp}@example.com",
        "password": "Pass1234",
        "role": "author"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("   [OK] Registration successful!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Username: {user_data['username']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Role: {user_data['role']}")
        else:
            print(f"   [FAIL] Registration failed: {response.json()}")
            return
    except requests.exceptions.ConnectionError:
        print("   [FAIL] Cannot connect to server. Is it running?")
        print("   Run: cd backend && .\\run.bat")
        return
    
    # Test 2: Login with credentials
    print("\n2. Testing User Login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data  # OAuth2PasswordRequestForm expects form data
    )
    
    if response.status_code == 200:
        print("   [OK] Login successful!")
        tokens = response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        print(f"   Access Token: {access_token[:50]}...")
        print(f"   Refresh Token: {refresh_token[:50]}...")
        
        # Debug: decode token to see payload
        try:
            from jose import jwt
            payload = jwt.decode(access_token, key="", options={"verify_signature": False})
            print(f"   DEBUG - Token payload: {payload}")
        except Exception as e:
            print(f"   DEBUG - Error decoding: {e}")
    else:
        print(f"   [FAIL] Login failed: {response.json()}")
        return
    
    # Test 3: Get current user info
    print("\n3. Testing Get Current User...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        print("   [OK] Retrieved user info!")
        user_info = response.json()
        print(f"   Username: {user_info['username']}")
        print(f"   Email: {user_info['email']}")
    else:
        print(f"   [FAIL] Failed to get user info: {response.json()}")
        return
    
    # Test 4: Update user profile
    print("\n4. Testing Update Profile...")
    update_data = {
        "bio": "I'm a test author writing amazing interactive novels!"
    }
    
    response = requests.put(
        f"{BASE_URL}/users/me",
        json=update_data,
        headers=headers
    )
    
    if response.status_code == 200:
        print("   [OK] Profile updated!")
        updated_user = response.json()
        print(f"   New bio: {updated_user['bio']}")
    else:
        print(f"   [FAIL] Profile update failed: {response.json()}")
    
    # Test 5: Refresh token
    print("\n5. Testing Token Refresh...")
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    if response.status_code == 200:
        print("   [OK] Token refreshed successfully!")
        new_tokens = response.json()
        print(f"   New Access Token: {new_tokens['access_token'][:50]}...")
    else:
        print(f"   [FAIL] Token refresh failed: {response.json()}")
    
    # Test 6: Get user by username
    print("\n6. Testing Get User By Username...")
    response = requests.get(f"{BASE_URL}/users/username/{register_data['username']}")
    
    if response.status_code == 200:
        print("   [OK] User found!")
        user_data = response.json()
        print(f"   Username: {user_data['username']}")
    else:
        print(f"   [FAIL] User not found: {response.json()}")
    
    print("\n" + "=" * 60)
    print("All authentication tests completed!")
    print("=" * 60)
    print("\nTry it yourself:")
    print(f"   1. Visit: http://localhost:8000/docs")
    print(f"   2. Test the endpoints interactively with Swagger UI")
    print("=" * 60)


if __name__ == "__main__":
    test_authentication_flow()

