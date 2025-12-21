from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user signup."""
    
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: Optional[str] = None


class LoginRequest(BaseModel):
    """Request schema for user login."""
    
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response schema for user data."""
    
    id: str
    email: str
    name: Optional[str] = None
    recommended_stage_id: Optional[str] = Field(None, alias="recommendedStageId")
    completed_milestones: list[str] = Field(default_factory=list, alias="completedMilestones")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""
    
    user: UserResponse
    token: str
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }