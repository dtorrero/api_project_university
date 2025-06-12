from app.connection.connection import MongoDBConnection
from typing import List, Optional, Dict
from bson import ObjectId

class SubjectController:
    def __init__(self):
        self.db = MongoDBConnection().get_database()
        self.collection = self.db.subjects

    def get_all_subjects(self) -> List[Dict]:
        """Get all subjects from the database"""
        subjects = list(self.collection.find())
        # Convert ObjectId to string for _id field
        for subject in subjects:
            if '_id' in subject:
                subject['_id'] = str(subject['_id'])
        return subjects

    def get_subject_by_id(self, id: int) -> Optional[Dict]:
        """Get a subject by its ID"""
        subject = self.collection.find_one({"id": id})
        if subject and '_id' in subject:
            subject['_id'] = str(subject['_id'])
        return subject

    def get_subjects_by_course(self, course_id: int) -> List[Dict]:
        """Get all subjects related to a specific course"""
        # First get the course to get its subjects list
        course = self.db.courses.find_one({"id": course_id})
        if not course:
            return []
        
        # Then get all subjects that are in the course's subjects list
        subjects = list(self.collection.find({"id": {"$in": course.get('subjects', [])}}))
        for subject in subjects:
            if '_id' in subject:
                subject['_id'] = str(subject['_id'])
        return subjects

    def get_subject_by_mongo_id(self, mongo_id: str) -> Optional[Dict]:
        """Get a subject by its MongoDB _id"""
        try:
            subject = self.collection.find_one({"_id": ObjectId(mongo_id)})
            if subject and '_id' in subject:
                subject['_id'] = str(subject['_id'])
            return subject
        except Exception as e:
            print(f"Error searching for subject by MongoDB ID: {str(e)}")
            return None

    def create_subject(self, subject_data: Dict) -> Dict:
        """Create a new subject in the database"""
        try:
            # Get the next available ID
            last_subject = self.collection.find_one(sort=[("id", -1)])
            next_id = 1 if not last_subject else last_subject["id"] + 1

            # Prepare subject data
            subject = {
                "id": next_id,
                "name": subject_data["name"],
                "description": subject_data["description"]
            }

            # Insert subject into database
            result = self.collection.insert_one(subject)
            
            # Get the created subject
            created_subject = self.collection.find_one({"_id": result.inserted_id})
            
            # Convert ObjectId to string for response
            if created_subject and '_id' in created_subject:
                created_subject["_id"] = str(created_subject["_id"])
            
            return created_subject
        except Exception as e:
            print(f"Error creating subject: {str(e)}")
            raise ValueError(f"Failed to create subject: {str(e)}")

    def update_subject(self, subject_id: int, subject_data: Dict) -> Optional[Dict]:
        """Update a subject by ID"""
        try:
            # Check if subject exists
            existing_subject = self.get_subject_by_id(subject_id)
            if not existing_subject:
                return None

            # Update subject in database
            update_result = self.collection.update_one(
                {"id": subject_id},
                {"$set": subject_data}
            )

            if update_result.modified_count == 0:
                return None

            # Get updated subject
            updated_subject = self.get_subject_by_id(subject_id)
            return updated_subject
        except Exception as e:
            print(f"Error updating subject: {str(e)}")
            raise ValueError(f"Failed to update subject: {str(e)}")

    def delete_subject(self, subject_id: int) -> bool:
        """Delete a subject by ID"""
        try:
            # Check if subject exists
            existing_subject = self.get_subject_by_id(subject_id)
            if not existing_subject:
                return False

            # Delete subject from database
            result = self.collection.delete_one({"id": subject_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting subject: {str(e)}")
            raise ValueError(f"Failed to delete subject: {str(e)}") 