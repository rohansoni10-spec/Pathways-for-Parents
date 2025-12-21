"""
Test script for Journey (Stages, Milestones, Progress) endpoints.
Tests Sprint 3 functionality.
"""

import asyncio
import httpx
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test credentials
TEST_EMAIL = f"journey_test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "TestPassword123!"


async def test_journey_endpoints():
    """Test all journey-related endpoints."""
    
    async with httpx.AsyncClient() as client:
        print("\n" + "="*60)
        print("SPRINT 3: JOURNEY STAGES & MILESTONE MANAGEMENT TESTS")
        print("="*60)
        
        # Step 1: Register a test user
        print("\n1. Registering test user...")
        register_response = await client.post(
            f"{BASE_URL}/api/v1/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        
        if register_response.status_code == 201:
            print(f"✓ User registered: {TEST_EMAIL}")
            token = register_response.json()["access_token"]
        else:
            print(f"✗ Registration failed: {register_response.status_code}")
            print(f"  Response: {register_response.text}")
            return
        
        # Headers with authentication
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Test GET /api/v1/stages (List all stages)
        print("\n2. Testing GET /api/v1/stages (List all stages)...")
        stages_response = await client.get(f"{BASE_URL}/api/v1/stages")
        
        if stages_response.status_code == 200:
            stages = stages_response.json()
            print(f"✓ Retrieved {len(stages)} stages")
            for stage in stages:
                print(f"  - {stage['title']} (Order: {stage['order']}, Age: {stage['age_range']})")
            
            # Save first stage ID for later tests
            if stages:
                first_stage_id = f"S{stages[0]['order']}"
                print(f"\n  Using stage ID '{first_stage_id}' for detailed tests")
        else:
            print(f"✗ Failed to retrieve stages: {stages_response.status_code}")
            print(f"  Response: {stages_response.text}")
            return
        
        # Step 3: Test GET /api/v1/stages/{stage_id} (Get specific stage)
        print(f"\n3. Testing GET /api/v1/stages/{first_stage_id} (Get specific stage)...")
        stage_detail_response = await client.get(f"{BASE_URL}/api/v1/stages/{first_stage_id}")
        
        if stage_detail_response.status_code == 200:
            stage_detail = stage_detail_response.json()
            print(f"✓ Retrieved stage details:")
            print(f"  Title: {stage_detail['title']}")
            print(f"  Description: {stage_detail['description'][:60]}...")
            print(f"  Age Range: {stage_detail['age_range']}")
        else:
            print(f"✗ Failed to retrieve stage details: {stage_detail_response.status_code}")
            print(f"  Response: {stage_detail_response.text}")
        
        # Step 4: Test GET /api/v1/milestones (List all milestones)
        print("\n4. Testing GET /api/v1/milestones (List all milestones)...")
        milestones_response = await client.get(f"{BASE_URL}/api/v1/milestones")
        
        if milestones_response.status_code == 200:
            all_milestones = milestones_response.json()
            print(f"✓ Retrieved {len(all_milestones)} total milestones")
            
            # Count by stage
            stage_counts = {}
            for milestone in all_milestones:
                stage_id = milestone['stage_id']
                stage_counts[stage_id] = stage_counts.get(stage_id, 0) + 1
            
            print("  Milestones per stage:")
            for stage_id, count in sorted(stage_counts.items()):
                print(f"    {stage_id}: {count} milestones")
        else:
            print(f"✗ Failed to retrieve milestones: {milestones_response.status_code}")
            print(f"  Response: {milestones_response.text}")
            return
        
        # Step 5: Test GET /api/v1/milestones?stageId=S1 (Filter by stage)
        print(f"\n5. Testing GET /api/v1/milestones?stageId={first_stage_id} (Filter by stage)...")
        filtered_milestones_response = await client.get(
            f"{BASE_URL}/api/v1/milestones",
            params={"stageId": first_stage_id}
        )
        
        if filtered_milestones_response.status_code == 200:
            filtered_milestones = filtered_milestones_response.json()
            print(f"✓ Retrieved {len(filtered_milestones)} milestones for {first_stage_id}")
            for i, milestone in enumerate(filtered_milestones[:3], 1):
                print(f"  {i}. {milestone['title']}")
            
            # Save first milestone ID for progress tests
            if filtered_milestones:
                first_milestone_id = filtered_milestones[0]['id']
                print(f"\n  Using milestone ID '{first_milestone_id}' for progress tests")
        else:
            print(f"✗ Failed to filter milestones: {filtered_milestones_response.status_code}")
            print(f"  Response: {filtered_milestones_response.text}")
            return
        
        # Step 6: Test GET /api/v1/milestones/{milestone_id} (Get specific milestone)
        print(f"\n6. Testing GET /api/v1/milestones/{first_milestone_id} (Get specific milestone)...")
        milestone_detail_response = await client.get(
            f"{BASE_URL}/api/v1/milestones/{first_milestone_id}"
        )
        
        if milestone_detail_response.status_code == 200:
            milestone_detail = milestone_detail_response.json()
            print(f"✓ Retrieved milestone details:")
            print(f"  Title: {milestone_detail['title']}")
            print(f"  Behavior: {milestone_detail['behavior'][:60]}...")
            print(f"  Stage: {milestone_detail['stage_id']}")
        else:
            print(f"✗ Failed to retrieve milestone details: {milestone_detail_response.status_code}")
            print(f"  Response: {milestone_detail_response.text}")
        
        # Step 7: Test GET /api/v1/progress (Get initial progress - should be empty)
        print("\n7. Testing GET /api/v1/progress (Get initial progress)...")
        initial_progress_response = await client.get(
            f"{BASE_URL}/api/v1/progress",
            headers=headers
        )
        
        if initial_progress_response.status_code == 200:
            initial_progress = initial_progress_response.json()
            print(f"✓ Retrieved initial progress:")
            print(f"  Completed milestones: {initial_progress['total_completed']}")
            print(f"  Total milestones: {initial_progress['total_milestones']}")
            print(f"  Stage progress: {len(initial_progress['stage_progress'])} stages tracked")
        else:
            print(f"✗ Failed to retrieve progress: {initial_progress_response.status_code}")
            print(f"  Response: {initial_progress_response.text}")
        
        # Step 8: Test POST /api/v1/progress/milestones/{milestone_id}/toggle (Mark complete)
        print(f"\n8. Testing POST /api/v1/progress/milestones/{first_milestone_id}/toggle (Mark complete)...")
        toggle_complete_response = await client.post(
            f"{BASE_URL}/api/v1/progress/milestones/{first_milestone_id}/toggle",
            headers=headers
        )
        
        if toggle_complete_response.status_code == 200:
            toggle_result = toggle_complete_response.json()
            print(f"✓ {toggle_result['message']}")
            print(f"  Milestone ID: {toggle_result['milestone_id']}")
            print(f"  Is completed: {toggle_result['is_completed']}")
        else:
            print(f"✗ Failed to toggle milestone: {toggle_complete_response.status_code}")
            print(f"  Response: {toggle_complete_response.text}")
        
        # Step 9: Test GET /api/v1/progress (Verify progress updated)
        print("\n9. Testing GET /api/v1/progress (Verify progress updated)...")
        updated_progress_response = await client.get(
            f"{BASE_URL}/api/v1/progress",
            headers=headers
        )
        
        if updated_progress_response.status_code == 200:
            updated_progress = updated_progress_response.json()
            print(f"✓ Retrieved updated progress:")
            print(f"  Completed milestones: {updated_progress['total_completed']}")
            print(f"  Completed IDs: {updated_progress['completed_milestone_ids']}")
            
            # Show stage progress
            for stage_id, progress in updated_progress['stage_progress'].items():
                if progress['completed_milestones'] > 0:
                    print(f"  {stage_id}: {progress['completed_milestones']}/{progress['total_milestones']} ({progress['percentage']}%)")
        else:
            print(f"✗ Failed to retrieve updated progress: {updated_progress_response.status_code}")
            print(f"  Response: {updated_progress_response.text}")
        
        # Step 10: Test POST /api/v1/progress/milestones/{milestone_id}/toggle (Mark incomplete)
        print(f"\n10. Testing POST /api/v1/progress/milestones/{first_milestone_id}/toggle (Mark incomplete)...")
        toggle_incomplete_response = await client.post(
            f"{BASE_URL}/api/v1/progress/milestones/{first_milestone_id}/toggle",
            headers=headers
        )
        
        if toggle_incomplete_response.status_code == 200:
            toggle_result = toggle_incomplete_response.json()
            print(f"✓ {toggle_result['message']}")
            print(f"  Is completed: {toggle_result['is_completed']}")
        else:
            print(f"✗ Failed to toggle milestone: {toggle_incomplete_response.status_code}")
            print(f"  Response: {toggle_incomplete_response.text}")
        
        # Step 11: Mark multiple milestones complete for reset test
        print("\n11. Marking multiple milestones complete for reset test...")
        if len(filtered_milestones) >= 3:
            for milestone in filtered_milestones[:3]:
                await client.post(
                    f"{BASE_URL}/api/v1/progress/milestones/{milestone['id']}/toggle",
                    headers=headers
                )
            print(f"✓ Marked 3 milestones as complete")
        
        # Step 12: Test DELETE /api/v1/progress (Reset all progress)
        print("\n12. Testing DELETE /api/v1/progress (Reset all progress)...")
        reset_response = await client.delete(
            f"{BASE_URL}/api/v1/progress",
            headers=headers
        )
        
        if reset_response.status_code == 200:
            reset_result = reset_response.json()
            print(f"✓ {reset_result['message']}")
            print(f"  Completed milestones after reset: {len(reset_result['completed_milestones'])}")
        else:
            print(f"✗ Failed to reset progress: {reset_response.status_code}")
            print(f"  Response: {reset_response.text}")
        
        # Step 13: Verify progress is reset
        print("\n13. Verifying progress is reset...")
        final_progress_response = await client.get(
            f"{BASE_URL}/api/v1/progress",
            headers=headers
        )
        
        if final_progress_response.status_code == 200:
            final_progress = final_progress_response.json()
            print(f"✓ Final progress check:")
            print(f"  Completed milestones: {final_progress['total_completed']}")
            if final_progress['total_completed'] == 0:
                print("  ✓ Progress successfully reset to zero")
        else:
            print(f"✗ Failed to verify reset: {final_progress_response.status_code}")
        
        print("\n" + "="*60)
        print("SPRINT 3 TESTS COMPLETED")
        print("="*60)


if __name__ == "__main__":
    print("\nStarting Journey endpoint tests...")
    print("Make sure the backend server is running on http://localhost:8000")
    print("And that the database has been seeded with stages and milestones.\n")
    
    asyncio.run(test_journey_endpoints())