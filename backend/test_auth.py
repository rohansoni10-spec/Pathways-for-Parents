"""
Test script for authentication endpoints.
Run this after starting the server with: python3 -m uvicorn main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_signup():
    """Test user signup endpoint."""
    print("\n=== Testing Signup ===")
    
    payload = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()["token"]
    return None


def test_login():
    """Test user login endpoint."""
    print("\n=== Testing Login ===")
    
    payload = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()["token"]
    return None


def test_get_me(token):
    """Test get current user endpoint."""
    print("\n=== Testing Get Me ===")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_logout(token):
    """Test logout endpoint."""
    print("\n=== Testing Logout ===")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_unauthorized_access():
    """Test accessing protected endpoint without token."""
    print("\n=== Testing Unauthorized Access ===")
    
    response = requests.get(f"{BASE_URL}/auth/me")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("Starting Authentication Tests...")
    print("=" * 50)
    
    # Test unauthorized access first
    test_unauthorized_access()
    
    # Test signup
    token = test_signup()
    
    if token:
        # Test get me with token from signup
        test_get_me(token)
        
        # Test logout
        test_logout(token)
    
    # Test login
    token = test_login()
    
    if token:
        # Test get me with token from login
        test_get_me(token)
    
    print("\n" + "=" * 50)
    print("Tests completed!")