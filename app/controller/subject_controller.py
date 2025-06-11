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