from fastapi import APIRouter, HTTPException, status
from app.services.user_service import UserService
from app.models.user import User, UserCreate
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        409: {"description": "Conflict - Email already exists"}
    },
)

user_service = UserService()

@router.get("/", response_model=List[User])
async def get_users():
    """Get all users"""
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/type/{user_type}", response_model=List[User])
async def get_users_by_type(user_type: str):
    """Get all users of a specific type (teacher/student)"""
    if user_type not in ["teacher", "student"]:
        raise HTTPException(status_code=400, detail="User type must be 'teacher' or 'student'")
    return user_service.get_users_by_type(user_type)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user with the following information:
    
    - **name**: User's full name (2-100 characters, letters only)
    - **email**: Valid email address
    - **type**: Either 'teacher' or 'student'
    - **courses**: Optional list of course IDs
    - **documents**: Optional list of document IDs
    """
    try:
        return user_service.create_user(user)
    except ValueError as e:
        if "Email already registered" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 