from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

from schemas.auth import SignupRequest, LoginRequest, AuthResponse, UserResponse
from models.user import User
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from dependencies.auth import get_current_user
from database import get_database


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """
    Register a new user account.
    
    - Validates email format and password length
    - Checks email uniqueness
    - Hashes password with Argon2
    - Creates user in MongoDB
    - Generates JWT token (30-day expiry)
    - Returns user data and token
    """
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user document
    now = datetime.now(timezone.utc)
    user = User(
        email=request.email,
        password_hash=password_hash,
        name=request.name,
        created_at=now,
        updated_at=now
    )
    
    # Insert into database
    result = await db.users.insert_one(user.to_dict())
    user_id = str(result.inserted_id)
    
    # Generate JWT token
    token = create_access_token(data={"sub": user_id})
    
    # Prepare response
    user_response = UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        recommended_stage_id=user.recommended_stage_id,
        completed_milestones=user.completed_milestones,
        created_at=user.created_at
    )
    
    return AuthResponse(user=user_response, token=token)


@router.post("/login", response_model=AuthResponse, response_model_by_alias=True)
async def login(request: LoginRequest):
    """
    Authenticate user and issue JWT token.
    
    - Validates email format
    - Verifies credentials
    - Generates JWT token (30-day expiry)
    - Returns user data and token
    """
    db = get_database()
    
    # Find user by email
    user_data = await db.users.find_one({"email": request.email})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Convert to User model
    user = User.from_mongo(user_data)
    user_id = str(user_data["_id"])
    
    # Generate JWT token
    token = create_access_token(data={"sub": user_id})
    
    # Prepare response
    user_response = UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        recommended_stage_id=user.recommended_stage_id,
        completed_milestones=user.completed_milestones,
        created_at=user.created_at
    )
    
    return AuthResponse(user=user_response, token=token)


@router.get("/me", response_model=UserResponse, response_model_by_alias=True)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile.
    
    Requires valid JWT token in Authorization header.
    Returns current user's profile data.
    """
    user_id = str(current_user.id)
    
    return UserResponse(
        id=user_id,
        email=current_user.email,
        name=current_user.name,
        recommended_stage_id=current_user.recommended_stage_id,
        completed_milestones=current_user.completed_milestones,
        created_at=current_user.created_at
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client-side token removal).
    
    Requires valid JWT token in Authorization header.
    Returns success message. Client should remove token from storage.
    """
    return {"message": "Logged out successfully"}