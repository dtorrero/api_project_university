from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Any, Annotated
from datetime import datetime
import re
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            raise ValueError("Invalid ObjectId")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator: Any) -> dict[str, Any]:
        return {"type": "string"}

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
        if not re.match(r'^[a-zA-Z\s\-\.]+$', v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and periods')
        return v.title()

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int = Field(..., description="User's unique identifier")
    mongo_id: Optional[PyObjectId] = Field(None, alias="_id", description="MongoDB document ID")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@university.edu",
                "type": "student",
                "courses": [1, 2],
                "documents": [1, 2]
            }
        } 