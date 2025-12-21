"""
Stages router - handles journey stage endpoints.
"""

from fastapi import APIRouter, HTTPException
from database import get_database
from models.stage import Stage

router = APIRouter(prefix="/api/v1/stages", tags=["stages"])


@router.get("", response_model=list[dict])
async def list_stages():
    """
    Get all journey stages, sorted by order.
    
    Returns:
        List of all stages with their details
    """
    db = get_database()
    stages_collection = db["stages"]
    
    # Fetch all stages sorted by order
    cursor = stages_collection.find({}).sort("order", 1)
    stages = await cursor.to_list(length=None)
    
    # Convert ObjectId to string for JSON serialization
    result = []
    for stage in stages:
        stage_dict = Stage.from_mongo(stage).model_dump(by_alias=True)
        # Convert _id to id for frontend
        if "_id" in stage_dict:
            stage_dict["id"] = stage_dict.pop("_id")
        result.append(stage_dict)
    
    return result


@router.get("/{stage_id}", response_model=dict)
async def get_stage(stage_id: str):
    """
    Get details of a specific stage.
    
    Args:
        stage_id: The stage identifier (e.g., "S1", "S2")
    
    Returns:
        Stage details
    
    Raises:
        HTTPException: 404 if stage not found
    """
    db = get_database()
    stages_collection = db["stages"]
    
    # Find stage by title matching the stage_id pattern
    # Stage IDs in seed data are like "S1", "S2", etc.
    # We need to find by order or by a custom field
    # For now, let's search by order (S1 = order 1, S2 = order 2, etc.)
    
    # Try to extract order from stage_id (e.g., "S1" -> 1)
    try:
        if stage_id.startswith("S"):
            order = int(stage_id[1:])
            stage = await stages_collection.find_one({"order": order})
        else:
            # If not in S# format, try to find by _id
            from bson import ObjectId
            if ObjectId.is_valid(stage_id):
                stage = await stages_collection.find_one({"_id": ObjectId(stage_id)})
            else:
                stage = None
    except (ValueError, IndexError):
        stage = None
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    # Convert to Stage model and then to dict
    stage_obj = Stage.from_mongo(stage)
    stage_dict = stage_obj.model_dump(by_alias=True)
    
    # Convert _id to id for frontend
    if "_id" in stage_dict:
        stage_dict["id"] = stage_dict.pop("_id")
    
    return stage_dict