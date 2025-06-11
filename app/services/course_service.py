from app.controller.course_controller import CourseController
from app.models.course import Course
from typing import List, Optional

class CourseService:
    def __init__(self):
        self.controller = CourseController()

    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        courses = self.controller.get_all_courses()
        return [Course(**course) for course in courses]

    def get_course_by_id(self, id: int) -> Optional[Course]:
        """Get a course by its ID"""
        course = self.controller.get_course_by_id(id)
        return Course(**course) if course else None

    def get_course_by_mongo_id(self, mongo_id: str) -> Optional[Course]:
        """Get a course by its MongoDB _id"""
        course = self.controller.get_course_by_mongo_id(mongo_id)
        return Course(**course) if course else None

    def get_courses_by_subject(self, subject_id: int) -> List[Course]:
        """Get all courses that include a specific subject"""
        courses = self.controller.get_courses_by_subject(subject_id)
        return [Course(**course) for course in courses] 