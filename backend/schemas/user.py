from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UpdateProfileRequest(BaseModel):
    """Request schema for updating user profile (name and/or email)."""
    
    name: Optional[str] = Field(None, description="User's display name")
    email: Optional[EmailStr] = Field(None, description="User's email address")


class ChangePasswordRequest(BaseModel):
    """Request schema for changing user password."""
    
    current_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


class MessageResponse(BaseModel):
    """Generic message response."""
    
    message: str