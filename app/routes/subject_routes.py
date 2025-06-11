from fastapi import APIRouter, HTTPException, status
from app.services.subject_service import SubjectService
from typing import List
from app.models.subject import Subject

router = APIRouter()
subject_service = SubjectService()

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