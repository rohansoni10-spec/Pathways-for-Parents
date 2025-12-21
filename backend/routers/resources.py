from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import get_database
from models.resource import Resource

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.get("")
async def get_resources(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title, description, and tags")
):
    """
    Get all resources with optional filtering by category and search.
    
    Query Parameters:
    - category: Filter by exact category match (e.g., "Diagnosis", "IEP")
    - search: Case-insensitive keyword search across title, description, and tags
    """
    db = get_database()
    resources_collection = db["resources"]
    
    # Build query filter
    query_filter = {}
    
    # Add category filter if provided
    if category:
        query_filter["category"] = category
    
    # Add search filter if provided
    if search:
        # Case-insensitive regex search across title, description, and tags
        search_regex = {"$regex": search, "$options": "i"}
        query_filter["$or"] = [
            {"title": search_regex},
            {"description": search_regex},
            {"tags": search_regex}
        ]
    
    # Fetch resources from database
    cursor = resources_collection.find(query_filter)
    resources_list = await cursor.to_list(length=None)
    
    # Convert to Resource models
    resources = [Resource.from_mongo(resource) for resource in resources_list]
    
    return resources


@router.get("/{resource_id}")
async def get_resource(resource_id: str):
    """
    Get a specific resource by ID.
    
    Path Parameters:
    - resource_id: The unique identifier of the resource
    """
    db = get_database()
    resources_collection = db["resources"]
    
    # Find resource by ID
    resource_data = await resources_collection.find_one({"_id": resource_id})
    
    if not resource_data:
        raise HTTPException(status_code=404, detail=f"Resource with id '{resource_id}' not found")
    
    # Convert to Resource model
    resource = Resource.from_mongo(resource_data)
    
    return resource