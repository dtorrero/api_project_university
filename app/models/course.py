from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated, List
from bson import ObjectId

class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Course name")
    subjects: List[int] = Field(..., description="List of subject IDs")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Course name")
    subjects: Optional[List[int]] = Field(None, description="List of subject IDs")

class Course(CourseBase):
    id: int = Field(..., description="Course's unique identifier")
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
                "name": "Computer Science",
                "subjects": [1, 2, 3, 4]
            }
        }
    ) 