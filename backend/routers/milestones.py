"""
Milestones router - handles milestone endpoints.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import get_database
from models.milestone import Milestone

router = APIRouter(prefix="/api/v1/milestones", tags=["milestones"])


@router.get("", response_model=list[dict])
async def list_milestones(stageId: Optional[str] = Query(None, description="Filter by stage ID")):
    """
    Get all milestones, optionally filtered by stage.
    
    Args:
        stageId: Optional stage ID to filter milestones (e.g., "S1", "S2")
    
    Returns:
        List of milestones
    """
    db = get_database()
    milestones_collection = db["milestones"]
    
    # Build query filter
    query = {}
    if stageId:
        query["stage_id"] = stageId
    
    # Fetch milestones
    cursor = milestones_collection.find(query)
    milestones = await cursor.to_list(length=None)
    
    # Convert to response format
    result = []
    for milestone in milestones:
        milestone_dict = Milestone.from_mongo(milestone).model_dump(by_alias=True)
        # Convert _id to id for frontend
        if "_id" in milestone_dict:
            milestone_dict["id"] = milestone_dict.pop("_id")
        result.append(milestone_dict)
    
    return result


@router.get("/{milestone_id}", response_model=dict)
async def get_milestone(milestone_id: str):
    """
    Get details of a specific milestone.
    
    Args:
        milestone_id: The milestone's MongoDB ObjectId
    
    Returns:
        Milestone details
    
    Raises:
        HTTPException: 404 if milestone not found
    """
    db = get_database()
    milestones_collection = db["milestones"]
    
    # Try to find by ObjectId
    from bson import ObjectId
    
    if not ObjectId.is_valid(milestone_id):
        raise HTTPException(status_code=400, detail="Invalid milestone ID format")
    
    milestone = await milestones_collection.find_one({"_id": ObjectId(milestone_id)})
    
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    # Convert to Milestone model and then to dict
    milestone_obj = Milestone.from_mongo(milestone)
    milestone_dict = milestone_obj.model_dump(by_alias=True)
    
    # Convert _id to id for frontend
    if "_id" in milestone_dict:
        milestone_dict["id"] = milestone_dict.pop("_id")
    
    return milestone_dict