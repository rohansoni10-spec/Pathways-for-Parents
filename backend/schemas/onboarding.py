from pydantic import BaseModel, Field
from datetime import datetime
from models.onboarding import ChildAgeRange, DiagnosisStatus, PrimaryConcern


class OnboardingRequest(BaseModel):
    """Schema for onboarding questionnaire request."""
    
    childAgeRange: ChildAgeRange = Field(
        ...,
        description="Child's age range",
        json_schema_extra={"example": "3-5y"}
    )
    diagnosisStatus: DiagnosisStatus = Field(
        ...,
        description="Current diagnosis status",
        json_schema_extra={"example": "waiting"}
    )
    primaryConcern: PrimaryConcern = Field(
        ...,
        description="Primary area of concern",
        json_schema_extra={"example": "speech"}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "childAgeRange": "3-5y",
                "diagnosisStatus": "waiting",
                "primaryConcern": "speech"
            }
        }


class OnboardingResponseSchema(BaseModel):
    """Schema for onboarding response."""
    
    id: str = Field(..., description="Onboarding response ID")
    userId: str = Field(..., description="User ID")
    childAgeRange: ChildAgeRange = Field(..., description="Child's age range")
    diagnosisStatus: DiagnosisStatus = Field(..., description="Diagnosis status")
    primaryConcern: PrimaryConcern = Field(..., description="Primary concern")
    recommendedStageId: str = Field(..., description="Recommended journey stage")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "userId": "507f191e810c19729de860ea",
                "childAgeRange": "3-5y",
                "diagnosisStatus": "waiting",
                "primaryConcern": "speech",
                "recommendedStageId": "s2",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            }
        }