from fastapi import APIRouter, HTTPException, status
from app.services.course_service import CourseService
from typing import List
from app.models.course import Course, CourseCreate, CourseUpdate
from pydantic import BaseModel

router = APIRouter()
course_service = CourseService()

class DeleteResponse(BaseModel):
    message: str

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

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED, tags=["courses"])
async def create_course(course: CourseCreate):
    """
    Create a new course with the following information:
    
    - **name**: Course name (1-100 characters)
    - **subjects**: List of subject IDs
    """
    try:
        return course_service.create_course(course)
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

@router.put("/{course_id}", response_model=Course, tags=["courses"])
async def update_course(course_id: int, course: CourseUpdate):
    """
    Update a course with the following information:
    
    - **name**: Course name (1-100 characters)
    - **subjects**: List of subject IDs
    """
    try:
        updated_course = course_service.update_course(course_id, course)
        if not updated_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return updated_course
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

@router.delete("/{course_id}", response_model=DeleteResponse, tags=["courses"])
async def delete_course(course_id: int):
    """Delete a course by ID"""
    try:
        deleted = course_service.delete_course(course_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return DeleteResponse(message=f"Course with ID {course_id} has been successfully deleted")
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