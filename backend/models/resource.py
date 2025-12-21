from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class ResourceCategory(str, Enum):
    """Allowed resource categories."""
    EARLY_INTERVENTION = "Early Intervention"
    DIAGNOSIS = "Diagnosis"
    INSURANCE = "Insurance"
    IEP = "IEP"
    THERAPY = "Therapy"
    GENERAL = "General"


class Resource(BaseModel):
    """Resource model for MongoDB."""
    
    id: str = Field(alias="_id")
    title: str
    description: str
    url: str
    category: ResourceCategory
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True)
        return data
    
    @classmethod
    def from_mongo(cls, data: dict) -> "Resource":
        """Create Resource instance from MongoDB document."""
        if not data:
            return None
        return cls(**data)