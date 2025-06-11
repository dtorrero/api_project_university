from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime
import re
from bson import ObjectId

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    type: str = Field(..., description="User type: 'teacher' or 'student'")
    courses: List[int] = Field(default_factory=list, description="List of course IDs")
    documents: List[int] = Field(default_factory=list, description="List of document IDs")

    @validator('type')
    def validate_type(cls, v):
        if v not in ['teacher', 'student']:
            raise ValueError('Type must be either "teacher" or "student"')
        return v

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s\-\.]+$', v):
            raise ValueError('Name can only contain letters, numbers, spaces, hyphens, and periods')
        return v.title()

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int = Field(..., description="User's unique identifier")
    mongo_id: Optional[str] = Field(None, alias="_id", description="MongoDB document ID")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            ObjectId: str
        },
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@university.edu",
                "type": "student",
                "courses": [1, 2],
                "documents": [1, 2]
            }
        }
    ) 