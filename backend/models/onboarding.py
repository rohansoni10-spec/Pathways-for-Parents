from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId


class ChildAgeRange(str, Enum):
    """Enum for child age ranges."""
    AGE_0_18M = "0-18m"
    AGE_18_36M = "18-36m"
    AGE_3_5Y = "3-5y"
    AGE_5_8Y = "5-8y"


class DiagnosisStatus(str, Enum):
    """Enum for diagnosis status."""
    NONE = "none"
    WAITING = "waiting"
    RECENT = "recent"  # <= 12 months
    ESTABLISHED = "established"  # > 12 months


class PrimaryConcern(str, Enum):
    """Enum for primary concerns."""
    SPEECH = "speech"
    BEHAVIOR = "behavior"
    SOCIAL = "social"
    SCHOOL = "school"
    GENERAL = "general"


class OnboardingResponse(BaseModel):
    """Onboarding response model for MongoDB."""
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId
    child_age_range: ChildAgeRange
    diagnosis_status: DiagnosisStatus
    primary_concern: PrimaryConcern
    recommended_stage_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude={"id"})
        if self.id:
            data["_id"] = self.id
        return data
    
    @classmethod
    def from_mongo(cls, data: dict) -> "OnboardingResponse":
        """Create OnboardingResponse instance from MongoDB document."""
        if not data:
            return None
        if "_id" in data:
            data["_id"] = str(data["_id"])
        if "user_id" in data:
            data["user_id"] = str(data["user_id"])
        return cls(**data)