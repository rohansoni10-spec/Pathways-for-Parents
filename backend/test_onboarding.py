"""
Test script for onboarding functionality and recommendation logic.

This script tests:
1. The recommendation algorithm with various input combinations
2. The onboarding API endpoints (POST and GET)

Run this script after starting the backend server:
    python test_onboarding.py
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test user credentials (you'll need to register first or use existing user)
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "TestPassword123!"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_test(test_name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"  → {details}")


def register_and_login() -> str:
    """Register a test user and get access token."""
    print_section("Authentication Setup")
    
    # Try to register (may fail if user exists)
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✓ User registered successfully")
        elif response.status_code == 400:
            print("ℹ User already exists, proceeding to login")
        else:
            print(f"⚠ Registration response: {response.status_code}")
    except Exception as e:
        print(f"⚠ Registration error: {e}")
    
    # Login to get token
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{API_BASE}/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["accessToken"]
        print("✓ Login successful")
        return token
    else:
        print(f"✗ Login failed: {response.status_code} - {response.text}")
        return None


def test_recommendation_logic():
    """Test the recommendation algorithm with various scenarios."""
    print_section("Recommendation Logic Tests")
    
    test_cases = [
        # Format: (age_range, diagnosis_status, primary_concern, expected_stage, description)
        
        # Base diagnosis status tests
        ("0-18m", "none", "general", "s1", "No diagnosis -> s1"),
        ("3-5y", "waiting", "general", "s2", "Waiting for diagnosis -> s2"),
        ("3-5y", "recent", "general", "s3", "Recent diagnosis -> s3"),
        ("5-8y", "established", "general", "s4", "Established diagnosis -> s4"),
        
        # Age guardrail tests (cap)
        ("0-18m", "established", "general", "s1", "Age cap: 0-18m max s1"),
        ("18-36m", "established", "general", "s2", "Age cap: 18-36m max s2"),
        ("3-5y", "established", "general", "s3", "Age cap: 3-5y max s3"),
        ("5-8y", "established", "general", "s4", "Age cap: 5-8y max s4"),
        
        # Concern override tests
        ("5-8y", "none", "school", "s4", "Override: school + 5-8y -> s4"),
        ("0-18m", "waiting", "speech", "s1", "Override: speech + <3y -> s1"),
        ("18-36m", "established", "speech", "s1", "Override: speech + <3y -> s1"),
        ("3-5y", "recent", "behavior", "s3", "Override: behavior + recent -> s3"),
        
        # Complex scenarios
        ("18-36m", "recent", "speech", "s1", "Speech override beats diagnosis"),
        ("5-8y", "waiting", "school", "s4", "School override beats diagnosis"),
        ("3-5y", "none", "behavior", "s1", "No override, base diagnosis"),
    ]
    
    passed = 0
    failed = 0
    
    for age_range, diagnosis_status, primary_concern, expected_stage, description in test_cases:
        # Import here to test the actual function
        from backend.models.onboarding import ChildAgeRange, DiagnosisStatus, PrimaryConcern
        from backend.utils.recommendation import calculate_recommended_stage
        
        # Convert string values to enums
        age_enum = ChildAgeRange(age_range)
        diagnosis_enum = DiagnosisStatus(diagnosis_status)
        concern_enum = PrimaryConcern(primary_concern)
        
        result = calculate_recommended_stage(age_enum, diagnosis_enum, concern_enum)
        
        if result == expected_stage:
            print_test(description, True, f"Got {result}")
            passed += 1
        else:
            print_test(description, False, f"Expected {expected_stage}, got {result}")
            failed += 1
    
    print(f"\nRecommendation Logic: {passed} passed, {failed} failed")
    return failed == 0


def test_onboarding_endpoints(token: str):
    """Test the onboarding API endpoints."""
    print_section("Onboarding API Endpoint Tests")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Submit onboarding (POST)
    onboarding_data = {
        "childAgeRange": "3-5y",
        "diagnosisStatus": "waiting",
        "primaryConcern": "speech"
    }
    
    response = requests.post(
        f"{API_BASE}/onboarding",
        json=onboarding_data,
        headers=headers
    )
    
    if response.status_code == 201:
        data = response.json()
        print_test(
            "POST /api/v1/onboarding",
            True,
            f"Created with recommended stage: {data['recommendedStageId']}"
        )
        
        # Verify the response structure
        required_fields = [
            "id", "userId", "childAgeRange", "diagnosisStatus",
            "primaryConcern", "recommendedStageId", "createdAt", "updatedAt"
        ]
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            print_test(
                "Response structure validation",
                False,
                f"Missing fields: {missing_fields}"
            )
        else:
            print_test("Response structure validation", True, "All fields present")
        
        # Verify recommendation logic
        expected_stage = "s1"  # speech + 3-5y should give s1 due to override
        if data["recommendedStageId"] == expected_stage:
            print_test(
                "Recommendation logic in API",
                True,
                f"Correctly calculated {expected_stage}"
            )
        else:
            print_test(
                "Recommendation logic in API",
                False,
                f"Expected {expected_stage}, got {data['recommendedStageId']}"
            )
    else:
        print_test(
            "POST /api/v1/onboarding",
            False,
            f"Status {response.status_code}: {response.text}"
        )
        return False
    
    # Test 2: Get onboarding (GET)
    response = requests.get(
        f"{API_BASE}/onboarding",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print_test(
            "GET /api/v1/onboarding",
            True,
            f"Retrieved onboarding with stage: {data['recommendedStageId']}"
        )
        
        # Verify it matches what we just submitted
        if (data["childAgeRange"] == onboarding_data["childAgeRange"] and
            data["diagnosisStatus"] == onboarding_data["diagnosisStatus"] and
            data["primaryConcern"] == onboarding_data["primaryConcern"]):
            print_test("Data consistency", True, "Retrieved data matches submitted data")
        else:
            print_test("Data consistency", False, "Retrieved data doesn't match")
    else:
        print_test(
            "GET /api/v1/onboarding",
            False,
            f"Status {response.status_code}: {response.text}"
        )
        return False
    
    # Test 3: Submit another onboarding (should update user's recommended stage)
    onboarding_data_2 = {
        "childAgeRange": "5-8y",
        "diagnosisStatus": "established",
        "primaryConcern": "school"
    }
    
    response = requests.post(
        f"{API_BASE}/onboarding",
        json=onboarding_data_2,
        headers=headers
    )
    
    if response.status_code == 201:
        data = response.json()
        expected_stage = "s4"  # school + 5-8y should give s4
        if data["recommendedStageId"] == expected_stage:
            print_test(
                "Multiple submissions",
                True,
                f"Second submission correctly calculated {expected_stage}"
            )
        else:
            print_test(
                "Multiple submissions",
                False,
                f"Expected {expected_stage}, got {data['recommendedStageId']}"
            )
    else:
        print_test(
            "Multiple submissions",
            False,
            f"Status {response.status_code}: {response.text}"
        )
    
    # Test 4: Verify GET returns the latest submission
    response = requests.get(
        f"{API_BASE}/onboarding",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["childAgeRange"] == onboarding_data_2["childAgeRange"]:
            print_test(
                "Latest submission retrieval",
                True,
                "GET returns the most recent onboarding"
            )
        else:
            print_test(
                "Latest submission retrieval",
                False,
                "GET doesn't return the latest submission"
            )
    
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("  ONBOARDING FUNCTIONALITY TEST SUITE")
    print("=" * 80)
    
    # Test 1: Recommendation Logic (unit tests)
    logic_passed = test_recommendation_logic()
    
    # Test 2: API Endpoints (integration tests)
    token = register_and_login()
    
    if token:
        api_passed = test_onboarding_endpoints(token)
    else:
        print("\n✗ Cannot test API endpoints without authentication")
        api_passed = False
    
    # Summary
    print_section("Test Summary")
    if logic_passed and api_passed:
        print("✓ All tests passed!")
    else:
        if not logic_passed:
            print("✗ Recommendation logic tests failed")
        if not api_passed:
            print("✗ API endpoint tests failed")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()