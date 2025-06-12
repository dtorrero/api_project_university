from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from bson import ObjectId

class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Subject name")
    description: str = Field(..., min_length=1, max_length=500, description="Subject description")

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Subject name")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Subject description")

class Subject(SubjectBase):
    id: int = Field(..., description="Subject's unique identifier")
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
                "name": "Programming Fundamentals",
                "description": "Introduction to programming concepts"
            }
        }
    ) 