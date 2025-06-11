from app.controller.subject_controller import SubjectController
from app.models.subject import Subject
from typing import List, Optional

class SubjectService:
    def __init__(self):
        self.controller = SubjectController()

    def get_all_subjects(self) -> List[Subject]:
        """Get all subjects"""
        subjects = self.controller.get_all_subjects()
        return [Subject(**subject) for subject in subjects]

    def get_subject_by_id(self, id: int) -> Optional[Subject]:
        """Get a subject by its ID"""
        subject = self.controller.get_subject_by_id(id)
        return Subject(**subject) if subject else None

    def get_subjects_by_course(self, course_id: int) -> List[Subject]:
        """Get all subjects related to a specific course"""
        subjects = self.controller.get_subjects_by_course(course_id)
        return [Subject(**subject) for subject in subjects]

    def get_subject_by_mongo_id(self, mongo_id: str) -> Optional[Subject]:
        """Get a subject by its MongoDB _id"""
        subject = self.controller.get_subject_by_mongo_id(mongo_id)
        return Subject(**subject) if subject else None 