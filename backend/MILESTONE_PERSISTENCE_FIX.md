# Milestone Persistence Fix

## Problem
Users reported that when they logged out and logged back in, their completed milestones were reset to 0. The progress they made in their child's journey was not being saved across sessions.

## Root Cause
The issue was a **field name mismatch** between the backend and frontend:

- **Backend** was using snake_case: `completed_milestones`, `recommended_stage_id`, `created_at`
- **Frontend** was expecting camelCase: `completedMilestones`, `recommendedStageId`, `createdAt`

When the backend sent the user data with snake_case field names, the frontend couldn't find the `completedMilestones` field, so it defaulted to an empty array.

## Solution
Updated the backend API responses to use camelCase field names by:

1. **Added Field Aliases** in [`schemas/auth.py`](schemas/auth.py):
   ```python
   class UserResponse(BaseModel):
       recommended_stage_id: Optional[str] = Field(None, alias="recommendedStageId")
       completed_milestones: list[str] = Field(default_factory=list, alias="completedMilestones")
       created_at: Optional[datetime] = Field(None, alias="createdAt")
       
       class Config:
           populate_by_name = True
   ```

2. **Enabled Alias Serialization** in [`routers/auth.py`](routers/auth.py) and [`routers/users.py`](routers/users.py):
   ```python
   @router.post("/login", response_model=AuthResponse, response_model_by_alias=True)
   @router.get("/me", response_model=UserResponse, response_model_by_alias=True)
   ```

## Files Modified

### Backend Changes:
- [`schemas/auth.py`](schemas/auth.py) - Added field aliases and Config
- [`routers/auth.py`](routers/auth.py) - Added `response_model_by_alias=True` to endpoints
- [`routers/users.py`](routers/users.py) - Added `response_model_by_alias=True` to endpoints

### Test Files Created:
- [`test_milestone_persistence.py`](test_milestone_persistence.py) - Comprehensive test for persistence

## Verification

The fix was verified by:

1. Creating a test user
2. Completing multiple milestones
3. Logging in again (simulating logout/login)
4. Confirming all completed milestones were returned

### API Response Before Fix:
```json
{
  "user": {
    "id": "...",
    "email": "user@example.com",
    "completed_milestones": ["m1", "m2"],  // ❌ Wrong field name
    "recommended_stage_id": "s1"           // ❌ Wrong field name
  }
}
```

### API Response After Fix:
```json
{
  "user": {
    "id": "...",
    "email": "user@example.com",
    "completedMilestones": ["m1", "m2"],  // ✅ Correct camelCase
    "recommendedStageId": "s1"            // ✅ Correct camelCase
  }
}
```

## Impact

✅ **Milestone progress now persists correctly across login sessions**
✅ **Frontend can properly read and display completed milestones**
✅ **Journey history tracking continues to work**
✅ **No breaking changes to database schema**
✅ **Backward compatible with existing data**

## Testing

Run the persistence test:
```bash
cd backend
pytest test_milestone_persistence.py -v
```

## Related Features

This fix ensures the following features work correctly:
- Journey progress tracking
- Milestone completion status
- Stage progress percentages
- User profile data
- Onboarding recommendations

## Notes

- The database still stores fields in snake_case (`completed_milestones`)
- Only the API responses use camelCase for frontend compatibility
- The `populate_by_name=True` config allows the backend to accept both formats