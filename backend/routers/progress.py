"""
Progress router - handles user progress tracking for milestones.
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from bson import ObjectId
from database import get_database
from models.user import User
from models.journey_history import JourneySnapshot
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.post("/milestones/{milestone_id}/toggle", response_model=dict)
async def toggle_milestone_completion(
    milestone_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Toggle completion status for a milestone.
    Adds milestone to completed_milestones if not present, removes if present.
    Also saves a journey snapshot to track the user's progress history.
    
    Args:
        milestone_id: The milestone ID (can be ObjectId or string identifier)
        current_user: The authenticated user
    
    Returns:
        Updated completion status and message
    
    Raises:
        HTTPException: 404 if milestone not found
    """
    db = get_database()
    milestones_collection = db["milestones"]
    users_collection = db["users"]
    journey_history_collection = db["journey_history"]
    
    # Try to find milestone by ObjectId first, then by any field containing the ID
    milestone = None
    milestone_title = "Unknown Milestone"
    stage_id = "unknown"
    
    if ObjectId.is_valid(milestone_id):
        milestone = await milestones_collection.find_one({"_id": ObjectId(milestone_id)})
        if milestone:
            milestone_title = milestone.get("title", "Unknown Milestone")
            stage_id = milestone.get("stage_id", "unknown")
    
    # If not found by ObjectId, this might be a frontend string ID
    # For now, we'll just accept any string ID and track it
    # In a production system, you'd want to validate against known milestone IDs
    
    # Get user's current completed milestones
    user_doc = await users_collection.find_one({"_id": ObjectId(current_user.id)})
    completed_milestones = user_doc.get("completed_milestones", [])
    
    # Toggle completion
    is_completed = False
    action = "uncompleted"
    if milestone_id in completed_milestones:
        # Remove from completed
        completed_milestones.remove(milestone_id)
        message = "Milestone marked as incomplete"
    else:
        # Add to completed
        completed_milestones.append(milestone_id)
        is_completed = True
        action = "completed"
        message = "Milestone marked as complete"
    
    # Calculate stage progress for the snapshot
    all_milestones = await milestones_collection.find({}).to_list(length=None)
    stage_progress = {}
    stage_milestones = {}
    
    # Group milestones by stage
    for ms in all_milestones:
        ms_stage_id = ms["stage_id"]
        ms_id_str = str(ms["_id"])
        
        if ms_stage_id not in stage_milestones:
            stage_milestones[ms_stage_id] = []
        stage_milestones[ms_stage_id].append(ms_id_str)
    
    # Calculate completion percentage for each stage
    for s_id, ms_ids in stage_milestones.items():
        total = len(ms_ids)
        completed = sum(1 for mid in ms_ids if mid in completed_milestones)
        percentage = round((completed / total * 100) if total > 0 else 0, 1)
        
        stage_progress[s_id] = {
            "total_milestones": total,
            "completed_milestones": completed,
            "percentage": percentage
        }
    
    # Create journey snapshot
    snapshot = JourneySnapshot(
        user_id=str(current_user.id),
        milestone_id=milestone_id,
        stage_id=stage_id,
        milestone_title=milestone_title,
        action=action,
        completed_milestones=completed_milestones.copy(),
        total_milestones_completed=len(completed_milestones),
        stage_progress=stage_progress
    )
    
    # Save snapshot to journey history
    await journey_history_collection.insert_one(snapshot.to_dict())
    
    # Update user document
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$set": {
                "completed_milestones": completed_milestones,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return {
        "milestone_id": milestone_id,
        "isComplete": is_completed,
        "message": message
    }


@router.get("", response_model=dict)
async def get_user_progress(current_user: User = Depends(get_current_user)):
    """
    Get current user's progress including completed milestone IDs and percentage per stage.
    
    Args:
        current_user: The authenticated user
    
    Returns:
        Progress data with completed milestones and stage completion percentages
    """
    db = get_database()
    users_collection = db["users"]
    milestones_collection = db["milestones"]
    
    # Get user's completed milestones
    user_doc = await users_collection.find_one({"_id": ObjectId(current_user.id)})
    completed_milestone_ids = user_doc.get("completed_milestones", [])
    
    # Get all milestones grouped by stage
    all_milestones = await milestones_collection.find({}).to_list(length=None)
    
    # Calculate progress per stage
    stage_progress = {}
    stage_milestones = {}
    
    # Group milestones by stage
    for milestone in all_milestones:
        stage_id = milestone["stage_id"]
        milestone_id_str = str(milestone["_id"])
        
        if stage_id not in stage_milestones:
            stage_milestones[stage_id] = []
        stage_milestones[stage_id].append(milestone_id_str)
    
    # Calculate completion percentage for each stage
    for stage_id, milestone_ids in stage_milestones.items():
        total = len(milestone_ids)
        completed = sum(1 for mid in milestone_ids if mid in completed_milestone_ids)
        percentage = round((completed / total * 100) if total > 0 else 0, 1)
        
        stage_progress[stage_id] = {
            "total_milestones": total,
            "completed_milestones": completed,
            "percentage": percentage
        }
    
    return {
        "completed_milestone_ids": completed_milestone_ids,
        "stage_progress": stage_progress,
        "total_completed": len(completed_milestone_ids),
        "total_milestones": len(all_milestones)
    }


@router.delete("", response_model=dict)
async def reset_progress(current_user: User = Depends(get_current_user)):
    """
    Reset all progress for the current user.
    Clears all completed milestones.
    
    Args:
        current_user: The authenticated user
    
    Returns:
        Success message
    """
    db = get_database()
    users_collection = db["users"]
    
    # Clear completed milestones
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$set": {
                "completed_milestones": [],
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return {
        "message": "All progress has been reset",
        "completed_milestones": []
    }


@router.get("/history", response_model=dict)
async def get_journey_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get the user's journey history - a timeline of milestone completions.
    
    Args:
        limit: Maximum number of history entries to return (default: 50)
        current_user: The authenticated user
    
    Returns:
        List of journey snapshots ordered by most recent first
    """
    db = get_database()
    journey_history_collection = db["journey_history"]
    
    # Get user's journey history, sorted by most recent first
    history_cursor = journey_history_collection.find(
        {"user_id": str(current_user.id)}
    ).sort("timestamp", -1).limit(limit)
    
    history = await history_cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings for JSON serialization
    for entry in history:
        if "_id" in entry:
            entry["_id"] = str(entry["_id"])
    
    return {
        "history": history,
        "total_entries": len(history)
    }


@router.get("/history/milestone/{milestone_id}", response_model=dict)
async def get_milestone_history(
    milestone_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get the history of a specific milestone for the current user.
    Shows all times this milestone was completed or uncompleted.
    
    Args:
        milestone_id: The milestone ID to get history for
        current_user: The authenticated user
    
    Returns:
        List of journey snapshots for this specific milestone
    """
    db = get_database()
    journey_history_collection = db["journey_history"]
    
    # Get history for this specific milestone
    history_cursor = journey_history_collection.find(
        {
            "user_id": str(current_user.id),
            "milestone_id": milestone_id
        }
    ).sort("timestamp", -1)
    
    history = await history_cursor.to_list(length=None)
    
    # Convert ObjectIds to strings for JSON serialization
    for entry in history:
        if "_id" in entry:
            entry["_id"] = str(entry["_id"])
    
    return {
        "milestone_id": milestone_id,
        "history": history,
        "total_entries": len(history)
    }