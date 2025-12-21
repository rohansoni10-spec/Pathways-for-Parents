"""
Test script for user profile management endpoints.
Tests GET /api/v1/users/me, PATCH /api/v1/users/me, and PATCH /api/v1/users/me/password
"""

import requests
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test user credentials
TEST_EMAIL = f"profile_test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Profile Test User"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_test(message):
    """Print test message in blue."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{message}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")


def print_success(message):
    """Print success message in green."""
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    """Print error message in red."""
    print(f"{RED}✗ {message}{RESET}")


def print_info(message):
    """Print info message in yellow."""
    print(f"{YELLOW}ℹ {message}{RESET}")


def signup_user():
    """Sign up a new test user."""
    print_test("TEST 1: Sign up new user")
    
    response = requests.post(
        f"{API_BASE}/auth/signup",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": TEST_NAME
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        print_success(f"User created: {data['user']['email']}")
        print_info(f"User ID: {data['user']['id']}")
        print_info(f"Name: {data['user']['name']}")
        return data["token"]
    else:
        print_error(f"Signup failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return None


def test_get_profile(token):
    """Test GET /api/v1/users/me endpoint."""
    print_test("TEST 2: Get user profile (GET /api/v1/users/me)")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/users/me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Profile retrieved successfully")
        print_info(f"Email: {data['email']}")
        print_info(f"Name: {data['name']}")
        print_info(f"ID: {data['id']}")
        return True
    else:
        print_error(f"Failed to get profile: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


def test_update_name(token):
    """Test updating user name."""
    print_test("TEST 3: Update user name (PATCH /api/v1/users/me)")
    
    new_name = "Updated Test User"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me",
        headers=headers,
        json={"name": new_name}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["name"] == new_name:
            print_success(f"Name updated successfully to: {data['name']}")
            return True
        else:
            print_error(f"Name not updated correctly. Expected: {new_name}, Got: {data['name']}")
            return False
    else:
        print_error(f"Failed to update name: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


def test_update_email(token):
    """Test updating user email."""
    print_test("TEST 4: Update user email (PATCH /api/v1/users/me)")
    
    new_email = f"updated_{datetime.now().timestamp()}@example.com"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me",
        headers=headers,
        json={"email": new_email}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["email"] == new_email:
            print_success(f"Email updated successfully to: {data['email']}")
            return True, new_email
        else:
            print_error(f"Email not updated correctly. Expected: {new_email}, Got: {data['email']}")
            return False, None
    else:
        print_error(f"Failed to update email: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False, None


def test_update_both(token):
    """Test updating both name and email."""
    print_test("TEST 5: Update both name and email (PATCH /api/v1/users/me)")
    
    new_name = "Both Updated User"
    new_email = f"both_updated_{datetime.now().timestamp()}@example.com"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me",
        headers=headers,
        json={"name": new_name, "email": new_email}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["name"] == new_name and data["email"] == new_email:
            print_success(f"Both fields updated successfully")
            print_info(f"Name: {data['name']}")
            print_info(f"Email: {data['email']}")
            return True
        else:
            print_error("Fields not updated correctly")
            return False
    else:
        print_error(f"Failed to update profile: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


def test_duplicate_email(token):
    """Test updating to an existing email (should fail)."""
    print_test("TEST 6: Update to duplicate email (should fail)")
    
    # Create another user first
    other_email = f"other_user_{datetime.now().timestamp()}@example.com"
    signup_response = requests.post(
        f"{API_BASE}/auth/signup",
        json={
            "email": other_email,
            "password": "password123",
            "name": "Other User"
        }
    )
    
    if signup_response.status_code != 201:
        print_error("Failed to create second user for test")
        return False
    
    # Try to update first user's email to the second user's email
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me",
        headers=headers,
        json={"email": other_email}
    )
    
    if response.status_code == 400:
        print_success("Duplicate email correctly rejected")
        print_info(f"Error message: {response.json().get('detail')}")
        return True
    else:
        print_error(f"Expected 400 status, got: {response.status_code}")
        return False


def test_change_password(token):
    """Test changing user password."""
    print_test("TEST 7: Change password (PATCH /api/v1/users/me/password)")
    
    new_password = "newpassword456"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me/password",
        headers=headers,
        json={
            "current_password": TEST_PASSWORD,
            "new_password": new_password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Password changed successfully: {data['message']}")
        return True, new_password
    else:
        print_error(f"Failed to change password: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False, None


def test_wrong_current_password(token):
    """Test changing password with wrong current password (should fail)."""
    print_test("TEST 8: Change password with wrong current password (should fail)")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me/password",
        headers=headers,
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword789"
        }
    )
    
    if response.status_code == 400:
        print_success("Wrong password correctly rejected")
        print_info(f"Error message: {response.json().get('detail')}")
        return True
    else:
        print_error(f"Expected 400 status, got: {response.status_code}")
        return False


def test_login_with_new_password(email, new_password):
    """Test logging in with the new password."""
    print_test("TEST 9: Login with new password")
    
    response = requests.post(
        f"{API_BASE}/auth/login",
        json={
            "email": email,
            "password": new_password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print_success("Login successful with new password")
        print_info(f"User: {data['user']['email']}")
        return True
    else:
        print_error(f"Login failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


def test_no_fields_update(token):
    """Test updating with no fields (should fail)."""
    print_test("TEST 10: Update with no fields (should fail)")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{API_BASE}/users/me",
        headers=headers,
        json={}
    )
    
    if response.status_code == 400:
        print_success("Empty update correctly rejected")
        print_info(f"Error message: {response.json().get('detail')}")
        return True
    else:
        print_error(f"Expected 400 status, got: {response.status_code}")
        return False


def main():
    """Run all profile management tests."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Starting Profile Management Tests{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = []
    
    # Sign up user
    token = signup_user()
    if not token:
        print_error("Cannot proceed without valid token")
        sys.exit(1)
    
    # Run tests
    results.append(("Get Profile", test_get_profile(token)))
    results.append(("Update Name", test_update_name(token)))
    success, new_email = test_update_email(token)
    results.append(("Update Email", success))
    results.append(("Update Both Fields", test_update_both(token)))
    results.append(("Duplicate Email Rejection", test_duplicate_email(token)))
    
    password_success, new_password = test_change_password(token)
    results.append(("Change Password", password_success))
    results.append(("Wrong Password Rejection", test_wrong_current_password(token)))
    
    if password_success and new_password:
        # Get the current email from the last update
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = requests.get(f"{API_BASE}/users/me", headers=headers)
        if profile_response.status_code == 200:
            current_email = profile_response.json()["email"]
            results.append(("Login with New Password", test_login_with_new_password(current_email, new_password)))
    
    results.append(("No Fields Update Rejection", test_no_fields_update(token)))
    
    # Print summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{test_name}: {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}All tests passed! ({passed}/{total}){RESET}")
    else:
        print(f"{YELLOW}Some tests failed. Passed: {passed}/{total}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)