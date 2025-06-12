from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Document title")
    file_url: str = Field(..., description="URL or path to the document file")
    type: str = Field(..., description="Document type (Lecture Notes, Assignment, Exam, Project, Study Guide)")
    grade: Optional[float] = Field(None, ge=0, le=100, description="Grade for the document (0-100)")
    teacher_id: int = Field(..., description="ID of the teacher who created the document")
    subject_id: int = Field(..., description="ID of the subject the document belongs to")
    owner: str = Field(..., description="ID of the user who owns the document (MongoDB ObjectId)")

    @validator('type')
    def validate_type(cls, v):
        valid_types = ['Lecture Notes', 'Assignment', 'Exam', 'Project', 'Study Guide']
        if v not in valid_types:
            raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Document title")
    file_url: Optional[str] = Field(None, description="URL or path to the document file")
    type: Optional[str] = Field(None, description="Document type (Lecture Notes, Assignment, Exam, Project, Study Guide)")
    grade: Optional[float] = Field(None, ge=0, le=100, description="Grade for the document (0-100)")
    teacher_id: Optional[int] = Field(None, description="ID of the teacher who created the document")
    subject_id: Optional[int] = Field(None, description="ID of the subject the document belongs to")
    owner: Optional[str] = Field(None, description="ID of the user who owns the document (MongoDB ObjectId)")

    @validator('type')
    def validate_type(cls, v):
        if v is not None:
            valid_types = ['Lecture Notes', 'Assignment', 'Exam', 'Project', 'Study Guide']
            if v not in valid_types:
                raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v

class Document(DocumentBase):
    id: int = Field(..., description="Document's unique identifier")
    upload_date: datetime = Field(default_factory=datetime.utcnow, description="Document upload date")
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
                "title": "Final Exam",
                "file_url": "https://example.com/exam.pdf",
                "type": "Exam",
                "grade": 85.0,
                "teacher_id": 1,
                "subject_id": 1,
                "owner": "507f1f77bcf86cd799439011",
                "upload_date": "2024-02-14T12:00:00"
            }
        }
    ) 