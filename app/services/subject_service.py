from app.controller.subject_controller import SubjectController
from app.models.subject import Subject, SubjectCreate, SubjectUpdate
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

    def create_subject(self, subject: SubjectCreate) -> Subject:
        """Create a new subject"""
        try:
            # Convert SubjectCreate to dict for controller
            subject_dict = subject.model_dump()
            
            # Create subject in database
            created_subject = self.controller.create_subject(subject_dict)
            
            # Convert to Subject model
            return Subject(**created_subject)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to create subject: {str(e)}")

    def update_subject(self, subject_id: int, subject_data: SubjectUpdate) -> Optional[Subject]:
        """Update a subject"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = {k: v for k, v in subject_data.model_dump().items() if v is not None}
            
            if not update_dict:
                raise ValueError("No valid fields to update")

            # Update subject in controller
            updated_subject = self.controller.update_subject(subject_id, update_dict)
            
            if not updated_subject:
                return None

            # Convert to Subject model and return
            return Subject(**updated_subject)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to update subject: {str(e)}")

    def delete_subject(self, subject_id: int) -> bool:
        """Delete a subject"""
        try:
            return self.controller.delete_subject(subject_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to delete subject: {str(e)}") 