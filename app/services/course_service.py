from app.controller.course_controller import CourseController
from app.models.course import Course, CourseCreate, CourseUpdate
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

    def create_course(self, course: CourseCreate) -> Course:
        """Create a new course"""
        try:
            # Convert CourseCreate to dict for controller
            course_dict = course.model_dump()
            
            # Create course in database
            created_course = self.controller.create_course(course_dict)
            
            # Convert to Course model
            return Course(**created_course)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to create course: {str(e)}")

    def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        """Update a course"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = {k: v for k, v in course_data.model_dump().items() if v is not None}
            
            if not update_dict:
                raise ValueError("No valid fields to update")

            # Update course in controller
            updated_course = self.controller.update_course(course_id, update_dict)
            
            if not updated_course:
                return None

            # Convert to Course model and return
            return Course(**updated_course)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to update course: {str(e)}")

    def delete_course(self, course_id: int) -> bool:
        """Delete a course"""
        try:
            return self.controller.delete_course(course_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to delete course: {str(e)}") 