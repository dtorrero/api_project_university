from fastapi import APIRouter, HTTPException, status
from app.services.subject_service import SubjectService
from typing import List
from app.models.subject import Subject, SubjectCreate, SubjectUpdate
from pydantic import BaseModel

router = APIRouter()
subject_service = SubjectService()

class DeleteResponse(BaseModel):
    message: str

@router.get("/", response_model=List[Subject])
async def get_subjects():
    """Get all subjects"""
    return subject_service.get_all_subjects()

@router.get("/id/{id}", response_model=Subject)
async def get_subject_by_id(id: int):
    """Get a subject by its ID"""
    subject = subject_service.get_subject_by_id(id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {id} not found"
        )
    return subject

@router.get("/mongo/{mongo_id}", response_model=Subject)
async def get_subject_by_mongo_id(mongo_id: str):
    """Get a subject by its MongoDB _id"""
    subject = subject_service.get_subject_by_mongo_id(mongo_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with MongoDB id {mongo_id} not found"
        )
    return subject

@router.get("/course/{course_id}", response_model=List[Subject])
async def get_subjects_by_course(course_id: int):
    """Get all subjects related to a specific course"""
    subjects = subject_service.get_subjects_by_course(course_id)
    if not subjects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No subjects found for course with id {course_id}"
        )
    return subjects

@router.post("/", response_model=Subject, status_code=status.HTTP_201_CREATED, tags=["subjects"])
async def create_subject(subject: SubjectCreate):
    """
    Create a new subject with the following information:
    
    - **name**: Subject name (1-100 characters)
    - **description**: Subject description (1-500 characters)
    """
    try:
        return subject_service.create_subject(subject)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{subject_id}", response_model=Subject, tags=["subjects"])
async def update_subject(subject_id: int, subject: SubjectUpdate):
    """
    Update a subject with the following information:
    
    - **name**: Subject name (1-100 characters)
    - **description**: Subject description (1-500 characters)
    """
    try:
        updated_subject = subject_service.update_subject(subject_id, subject)
        if not updated_subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject with ID {subject_id} not found"
            )
        return updated_subject
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{subject_id}", response_model=DeleteResponse, tags=["subjects"])
async def delete_subject(subject_id: int):
    """Delete a subject by ID"""
    try:
        deleted = subject_service.delete_subject(subject_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject with ID {subject_id} not found"
            )
        return DeleteResponse(message=f"Subject with ID {subject_id} has been successfully deleted")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 