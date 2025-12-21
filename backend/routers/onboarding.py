from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from bson import ObjectId

from models.user import User
from models.onboarding import OnboardingResponse
from schemas.onboarding import OnboardingRequest, OnboardingResponseSchema
from dependencies.auth import get_current_user
from database import get_database
from utils.recommendation import calculate_recommended_stage


router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])


@router.post("", response_model=OnboardingResponseSchema, status_code=status.HTTP_201_CREATED)
async def submit_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(get_current_user)
) -> OnboardingResponseSchema:
    """
    Submit onboarding questionnaire responses.
    
    Calculates the recommended journey stage based on:
    - Child's age range
    - Diagnosis status
    - Primary concern
    
    Saves the response and updates the user's recommended_stage_id.
    
    Args:
        request: Onboarding questionnaire responses
        current_user: Authenticated user from JWT token
        
    Returns:
        OnboardingResponseSchema with calculated recommendation
        
    Raises:
        HTTPException: 500 if database operation fails
    """
    db = get_database()
    
    # Calculate recommended stage using the deterministic algorithm
    recommended_stage_id = calculate_recommended_stage(
        age_range=request.childAgeRange,
        diagnosis_status=request.diagnosisStatus,
        primary_concern=request.primaryConcern
    )
    
    # Create onboarding response document
    onboarding_response = OnboardingResponse(
        user_id=current_user.id,
        child_age_range=request.childAgeRange,
        diagnosis_status=request.diagnosisStatus,
        primary_concern=request.primaryConcern,
        recommended_stage_id=recommended_stage_id
    )
    
    try:
        # Save onboarding response to database
        result = await db.onboarding_responses.insert_one(
            onboarding_response.to_dict()
        )
        onboarding_response.id = result.inserted_id
        
        # Update user's recommended_stage_id
        await db.users.update_one(
            {"_id": current_user.id},
            {
                "$set": {
                    "recommended_stage_id": recommended_stage_id,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save onboarding response: {str(e)}"
        )
    
    # Return response in camelCase format
    return OnboardingResponseSchema(
        id=str(onboarding_response.id),
        userId=str(onboarding_response.user_id),
        childAgeRange=onboarding_response.child_age_range,
        diagnosisStatus=onboarding_response.diagnosis_status,
        primaryConcern=onboarding_response.primary_concern,
        recommendedStageId=onboarding_response.recommended_stage_id,
        createdAt=onboarding_response.created_at,
        updatedAt=onboarding_response.updated_at
    )


@router.get("", response_model=OnboardingResponseSchema)
async def get_onboarding(
    current_user: User = Depends(get_current_user)
) -> OnboardingResponseSchema:
    """
    Get the user's latest onboarding response.
    
    Args:
        current_user: Authenticated user from JWT token
        
    Returns:
        OnboardingResponseSchema with the latest onboarding response
        
    Raises:
        HTTPException: 404 if no onboarding response found
    """
    db = get_database()
    
    # Find the most recent onboarding response for this user
    onboarding_data = await db.onboarding_responses.find_one(
        {"user_id": current_user.id},
        sort=[("created_at", -1)]  # Sort by created_at descending (most recent first)
    )
    
    if not onboarding_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No onboarding response found for this user"
        )
    
    # Convert MongoDB document to OnboardingResponse model
    onboarding_response = OnboardingResponse.from_mongo(onboarding_data)
    
    # Return response in camelCase format
    return OnboardingResponseSchema(
        id=str(onboarding_response.id),
        userId=str(onboarding_response.user_id),
        childAgeRange=onboarding_response.child_age_range,
        diagnosisStatus=onboarding_response.diagnosis_status,
        primaryConcern=onboarding_response.primary_concern,
        recommendedStageId=onboarding_response.recommended_stage_id,
        createdAt=onboarding_response.created_at,
        updatedAt=onboarding_response.updated_at
    )