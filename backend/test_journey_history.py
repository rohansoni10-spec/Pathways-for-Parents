"""
Test journey history functionality.
Tests the journey snapshot creation and retrieval endpoints.
Run this after starting the server with: python -m uvicorn main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def get_auth_token():
    """Get authentication token by logging in or registering."""
    print("\n=== Getting Auth Token ===")
    
    # Try to signup a new user
    signup_payload = {
        "email": "journey_test@example.com",
        "password": "TestPass123!",
        "name": "Journey Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload)
    
    if response.status_code == 201:
        print("✓ New user registered")
        return response.json()["token"]
    
    # If signup fails (user exists), try login
    login_payload = {
        "email": "journey_test@example.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    
    if response.status_code == 200:
        print("✓ Logged in with existing user")
        return response.json()["token"]
    
    print("✗ Failed to get auth token")
    return None


def test_milestone_completion_creates_history(token):
    """Test that completing a milestone creates a journey history entry."""
    print("\n=== Test: Milestone Completion Creates History ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Complete a milestone
    response = requests.post(
        f"{BASE_URL}/progress/milestones/m1-1/toggle",
        headers=headers
    )
    
    print(f"Toggle milestone status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Milestone completed: {data.get('isComplete')}")
        print(f"  Message: {data.get('message')}")
    
    # Check that history was created
    response = requests.get(f"{BASE_URL}/progress/history", headers=headers)
    
    print(f"Get history status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Total history entries: {data.get('total_entries')}")
        
        if data.get('history'):
            latest = data['history'][0]
            print(f"  Latest entry:")
            print(f"    - Milestone ID: {latest.get('milestone_id')}")
            print(f"    - Action: {latest.get('action')}")
            print(f"    - Total completed: {latest.get('total_milestones_completed')}")
            print(f"    - Timestamp: {latest.get('timestamp')}")
            print("  ✓ History entry created successfully")
        else:
            print("  ✗ No history entries found")
    else:
        print(f"  ✗ Failed to get history: {response.text}")


def test_milestone_uncomplete_creates_history(token):
    """Test that uncompleting a milestone creates a history entry."""
    print("\n=== Test: Milestone Uncomplete Creates History ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Complete a milestone first
    milestone_id = "m1-2"
    requests.post(
        f"{BASE_URL}/progress/milestones/{milestone_id}/toggle",
        headers=headers
    )
    
    # Uncomplete the milestone
    response = requests.post(
        f"{BASE_URL}/progress/milestones/{milestone_id}/toggle",
        headers=headers
    )
    
    print(f"Toggle milestone status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Milestone completed: {data.get('isComplete')}")
        print(f"  Message: {data.get('message')}")
    
    # Check history for uncomplete action
    response = requests.get(f"{BASE_URL}/progress/history", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Find the uncomplete entry
        uncomplete_entry = None
        for entry in data.get('history', []):
            if entry.get('milestone_id') == milestone_id and entry.get('action') == 'uncompleted':
                uncomplete_entry = entry
                break
        
        if uncomplete_entry:
            print(f"  ✓ Found uncomplete entry for {milestone_id}")
            print(f"    - Action: {uncomplete_entry.get('action')}")
            print(f"    - Milestone in completed list: {milestone_id in uncomplete_entry.get('completed_milestones', [])}")
        else:
            print(f"  ✗ No uncomplete entry found for {milestone_id}")


def test_get_milestone_specific_history(token):
    """Test retrieving history for a specific milestone."""
    print("\n=== Test: Get Milestone Specific History ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    milestone_id = "m1-3"
    
    # Toggle milestone multiple times
    print(f"  Toggling {milestone_id} multiple times...")
    for i in range(3):
        requests.post(
            f"{BASE_URL}/progress/milestones/{milestone_id}/toggle",
            headers=headers
        )
    
    # Get history for this specific milestone
    response = requests.get(
        f"{BASE_URL}/progress/history/milestone/{milestone_id}",
        headers=headers
    )
    
    print(f"Get milestone history status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Milestone ID: {data.get('milestone_id')}")
        print(f"  Total entries: {data.get('total_entries')}")
        
        if data.get('history'):
            print(f"  Actions sequence:")
            for entry in data['history']:
                print(f"    - {entry.get('action')} at {entry.get('timestamp')}")
            print("  ✓ Milestone-specific history retrieved successfully")
        else:
            print("  ✗ No history entries found")
    else:
        print(f"  ✗ Failed to get milestone history: {response.text}")


def test_history_limit_parameter(token):
    """Test that the limit parameter works correctly."""
    print("\n=== Test: History Limit Parameter ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create multiple history entries
    print("  Creating multiple history entries...")
    for i in range(5):
        requests.post(
            f"{BASE_URL}/progress/milestones/m2-{i}/toggle",
            headers=headers
        )
    
    # Get history with limit
    response = requests.get(
        f"{BASE_URL}/progress/history?limit=3",
        headers=headers
    )
    
    print(f"Get history with limit status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        entries_count = len(data.get('history', []))
        print(f"  Requested limit: 3")
        print(f"  Entries returned: {entries_count}")
        
        if entries_count <= 3:
            print("  ✓ Limit parameter working correctly")
        else:
            print(f"  ✗ Returned {entries_count} entries, expected <= 3")
    else:
        print(f"  ✗ Failed to get history: {response.text}")


def test_history_includes_stage_progress(token):
    """Test that history entries include stage progress information."""
    print("\n=== Test: History Includes Stage Progress ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Complete a milestone
    requests.post(
        f"{BASE_URL}/progress/milestones/m1-1/toggle",
        headers=headers
    )
    
    # Get history
    response = requests.get(f"{BASE_URL}/progress/history", headers=headers)
    
    print(f"Get history status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        
        if data.get('history'):
            latest_entry = data['history'][0]
            stage_progress = latest_entry.get('stage_progress', {})
            
            print(f"  Stage progress included: {bool(stage_progress)}")
            
            if stage_progress:
                print(f"  Number of stages tracked: {len(stage_progress)}")
                
                # Show first stage's progress
                first_stage = list(stage_progress.keys())[0]
                stage_data = stage_progress[first_stage]
                print(f"  Sample stage ({first_stage}):")
                print(f"    - Total milestones: {stage_data.get('total_milestones')}")
                print(f"    - Completed: {stage_data.get('completed_milestones')}")
                print(f"    - Percentage: {stage_data.get('percentage')}%")
                print("  ✓ Stage progress data included correctly")
            else:
                print("  ✗ No stage progress data found")
        else:
            print("  ✗ No history entries found")
    else:
        print(f"  ✗ Failed to get history: {response.text}")


def cleanup_test_data(token):
    """Reset progress to clean up test data."""
    print("\n=== Cleaning Up Test Data ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(f"{BASE_URL}/progress", headers=headers)
    
    if response.status_code == 200:
        print("  ✓ Test data cleaned up successfully")
    else:
        print(f"  ⚠ Cleanup may have failed: {response.status_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("Starting Journey History Tests...")
    print("=" * 60)
    
    # Get authentication token
    token = get_auth_token()
    
    if not token:
        print("\n✗ Failed to get authentication token. Exiting.")
        exit(1)
    
    # Run tests
    test_milestone_completion_creates_history(token)
    test_milestone_uncomplete_creates_history(token)
    test_get_milestone_specific_history(token)
    test_history_limit_parameter(token)
    test_history_includes_stage_progress(token)
    
    # Cleanup
    cleanup_test_data(token)
    
    print("\n" + "=" * 60)
    print("Journey History Tests Completed!")
    print("=" * 60)