"""
Test NailsDash API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User",
        "phone": "+1234567890"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    return None

def test_get_current_user(access_token):
    """Test getting current user info"""
    print("\n=== Testing Get Current User ===")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_duplicate_registration():
    """Test duplicate user registration (should fail)"""
    print("\n=== Testing Duplicate Registration (Should Fail) ===")
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 400

def test_invalid_login():
    """Test login with invalid credentials (should fail)"""
    print("\n=== Testing Invalid Login (Should Fail) ===")
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 401

def main():
    """Run all tests"""
    print("=" * 60)
    print("NailsDash API Testing")
    print("=" * 60)
    
    results = []
    
    # Test basic endpoints
    results.append(("Health Check", test_health_check()))
    results.append(("Root Endpoint", test_root()))
    
    # Test authentication flow
    results.append(("User Registration", test_register()))
    access_token = test_login()
    results.append(("User Login", access_token is not None))
    
    if access_token:
        results.append(("Get Current User", test_get_current_user(access_token)))
    
    # Test error cases
    results.append(("Duplicate Registration", test_duplicate_registration()))
    results.append(("Invalid Login", test_invalid_login()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
