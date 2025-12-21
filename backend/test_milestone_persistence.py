"""
Test to verify milestone completion persists across login sessions.
This test validates the fix for the camelCase field name issue.
"""

import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_milestone_persistence_across_sessions():
    """
    Test that completed milestones persist when user logs out and logs back in.
    
    Steps:
    1. Create a new user
    2. Complete some milestones
    3. Simulate logout (get new token via login)
    4. Verify milestones are still present
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Step 1: Create a new user
        signup_response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "persistence_test@example.com",
                "password": "testpass123",
                "name": "Persistence Test User"
            }
        )
        assert signup_response.status_code == 201
        signup_data = signup_response.json()
        token1 = signup_data["token"]
        user_id = signup_data["user"]["id"]
        
        # Verify initial state - no completed milestones
        assert signup_data["user"]["completedMilestones"] == []
        
        # Step 2: Complete some milestones
        headers = {"Authorization": f"Bearer {token1}"}
        
        # Complete milestone 1
        toggle1 = await client.post(
            "/api/v1/progress/milestones/milestone-1/toggle",
            headers=headers
        )
        assert toggle1.status_code == 200
        assert toggle1.json()["isComplete"] is True
        
        # Complete milestone 2
        toggle2 = await client.post(
            "/api/v1/progress/milestones/milestone-2/toggle",
            headers=headers
        )
        assert toggle2.status_code == 200
        assert toggle2.json()["isComplete"] is True
        
        # Complete milestone 3
        toggle3 = await client.post(
            "/api/v1/progress/milestones/milestone-3/toggle",
            headers=headers
        )
        assert toggle3.status_code == 200
        assert toggle3.json()["isComplete"] is True
        
        # Verify milestones are saved
        me_response = await client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert len(me_data["completedMilestones"]) == 3
        assert "milestone-1" in me_data["completedMilestones"]
        assert "milestone-2" in me_data["completedMilestones"]
        assert "milestone-3" in me_data["completedMilestones"]
        
        # Step 3: Simulate logout and login (get new token)
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "persistence_test@example.com",
                "password": "testpass123"
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        token2 = login_data["token"]
        
        # Verify tokens are different (simulating new session)
        assert token1 != token2
        
        # Step 4: Verify milestones persisted after "logout/login"
        assert login_data["user"]["id"] == user_id
        assert len(login_data["user"]["completedMilestones"]) == 3
        assert "milestone-1" in login_data["user"]["completedMilestones"]
        assert "milestone-2" in login_data["user"]["completedMilestones"]
        assert "milestone-3" in login_data["user"]["completedMilestones"]
        
        # Also verify with /me endpoint using new token
        new_headers = {"Authorization": f"Bearer {token2}"}
        me_response2 = await client.get("/api/v1/auth/me", headers=new_headers)
        assert me_response2.status_code == 200
        me_data2 = me_response2.json()
        assert len(me_data2["completedMilestones"]) == 3
        assert "milestone-1" in me_data2["completedMilestones"]
        assert "milestone-2" in me_data2["completedMilestones"]
        assert "milestone-3" in me_data2["completedMilestones"]
        
        print("✅ Milestone persistence test passed!")
        print(f"   User completed 3 milestones, logged out, logged back in")
        print(f"   All 3 milestones were successfully restored")