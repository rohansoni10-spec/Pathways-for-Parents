"""
Users router - handles user profile management.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

from schemas.user import UpdateProfileRequest, ChangePasswordRequest, MessageResponse
from schemas.auth import UserResponse
from models.user import User
from utils.security import hash_password, verify_password
from dependencies.auth import get_current_user
from database import get_database


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_model=UserResponse, response_model_by_alias=True)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile (alias for /auth/me).
    
    Requires valid JWT token in Authorization header.
    Returns current user's profile data.
    """
    user_id = str(current_user.id)
    
    return UserResponse(
        id=user_id,
        email=current_user.email,
        name=current_user.name,
        recommended_stage_id=current_user.recommended_stage_id,
        completed_milestones=current_user.completed_milestones,
        created_at=current_user.created_at
    )


@router.patch("/me", response_model=UserResponse, response_model_by_alias=True)
async def update_user_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile (name and/or email).
    
    - Updates user's name and/or email
    - Validates email format and uniqueness (if changed)
    - Returns updated user object
    
    Args:
        request: UpdateProfileRequest with optional name and email
        current_user: The authenticated user
    
    Returns:
        Updated user profile
    
    Raises:
        HTTPException: 400 if no fields provided or email already exists
    """
    db = get_database()
    users_collection = db["users"]
    
    # Check if at least one field is provided
    if request.name is None and request.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (name or email) must be provided"
        )
    
    update_data = {"updated_at": datetime.now(timezone.utc)}
    
    # Update name if provided
    if request.name is not None:
        update_data["name"] = request.name
    
    # Update email if provided and validate uniqueness
    if request.email is not None:
        # Check if email is different from current
        if request.email != current_user.email:
            # Check if new email already exists (excluding current user)
            existing_user = await users_collection.find_one({
                "email": request.email,
                "_id": {"$ne": ObjectId(current_user.id)}
            })
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            update_data["email"] = request.email
    
    # Update user document
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user_data = await users_collection.find_one({"_id": ObjectId(current_user.id)})
    updated_user = User.from_mongo(updated_user_data)
    
    return UserResponse(
        id=str(updated_user.id),
        email=updated_user.email,
        name=updated_user.name,
        recommended_stage_id=updated_user.recommended_stage_id,
        completed_milestones=updated_user.completed_milestones,
        created_at=updated_user.created_at
    )


@router.patch("/me/password", response_model=MessageResponse)
async def change_user_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Change user password.
    
    - Verifies current password
    - Validates new password (minimum 8 characters)
    - Updates password hash with Argon2
    - Returns success message
    
    Args:
        request: ChangePasswordRequest with current and new passwords
        current_user: The authenticated user
    
    Returns:
        Success message
    
    Raises:
        HTTPException: 400 if current password is incorrect
    """
    db = get_database()
    users_collection = db["users"]
    
    # Get user's current password hash
    user_data = await users_collection.find_one({"_id": ObjectId(current_user.id)})
    
    # Verify current password
    if not verify_password(request.current_password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    new_password_hash = hash_password(request.new_password)
    
    # Update password hash
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$set": {
                "password_hash": new_password_hash,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return MessageResponse(message="Password changed successfully")