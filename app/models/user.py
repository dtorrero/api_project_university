from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime
import re
from bson import ObjectId

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    type: str = Field(..., description="User type (teacher/student)")
    courses: Optional[List[int]] = Field(default=[], description="List of course IDs")
    documents: Optional[List[int]] = Field(default=[], description="List of document IDs")

    @validator('type')
    def type_must_be_valid(cls, v):
        if v not in ['teacher', 'student']:
            raise ValueError('Type must be either "teacher" or "student"')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    type: Optional[str] = Field(None, description="User type (teacher/student)")
    courses: Optional[List[int]] = Field(None, description="List of course IDs")
    documents: Optional[List[int]] = Field(None, description="List of document IDs")

    @validator('type')
    def type_must_be_valid(cls, v):
        if v is not None and v not in ['teacher', 'student']:
            raise ValueError('Type must be either "teacher" or "student"')
        return v

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
                "email": "john@example.com",
                "type": "teacher",
                "courses": [1, 2, 3],
                "documents": [1, 2]
            }
        }
    ) 