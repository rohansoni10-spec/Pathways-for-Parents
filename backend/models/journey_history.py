from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom type for MongoDB ObjectId that works with Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, _):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _handler):
        return {"type": "string"}


class JourneySnapshot(BaseModel):
    """
    Journey snapshot model for MongoDB.
    Captures the state of a user's journey at the moment a milestone is completed.
    """
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str  # Reference to the user
    milestone_id: str  # The milestone that was just completed
    stage_id: str  # The stage this milestone belongs to
    milestone_title: str  # Title of the completed milestone
    action: str  # "completed" or "uncompleted"
    completed_milestones: list[str]  # Snapshot of all completed milestones at this moment
    total_milestones_completed: int  # Total count at this moment
    stage_progress: dict  # Progress per stage at this moment
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
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
    def from_mongo(cls, data: dict) -> "JourneySnapshot":
        """Create JourneySnapshot instance from MongoDB document."""
        if not data:
            return None
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)