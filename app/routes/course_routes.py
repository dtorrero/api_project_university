from fastapi import APIRouter, HTTPException, status
from app.services.course_service import CourseService
from typing import List
from app.models.course import Course

router = APIRouter()
course_service = CourseService()

@router.get("/", response_model=List[Course], tags=["courses"])
async def get_courses():
    """Get all courses"""
    return course_service.get_all_courses()

@router.get("/id/{id}", response_model=Course, tags=["courses"])
async def get_course_by_id(id: int):
    """Get a course by its ID"""
    course = course_service.get_course_by_id(id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {id} not found"
        )
    return course

@router.get("/mongo/{mongo_id}", response_model=Course, tags=["courses"])
async def get_course_by_mongo_id(mongo_id: str):
    """Get a course by its MongoDB _id"""
    course = course_service.get_course_by_mongo_id(mongo_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with MongoDB ID {mongo_id} not found"
        )
    return course

@router.get("/subject/{subject_id}", response_model=List[Course], tags=["courses"])
async def get_courses_by_subject(subject_id: int):
    """Get all courses that include a specific subject"""
    courses = course_service.get_courses_by_subject(subject_id)
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No courses found for subject ID {subject_id}"
        )
    return courses 