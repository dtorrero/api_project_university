from app.connection.connection import MongoDBConnection
from typing import List, Optional, Dict
from bson import ObjectId

class CourseController:
    def __init__(self):
        self.db = MongoDBConnection().get_database()
        self.collection = self.db.courses

    def get_all_courses(self) -> List[Dict]:
        """Get all courses from the database"""
        courses = list(self.collection.find())
        # Convert ObjectId to string for _id field
        for course in courses:
            if '_id' in course:
                course['_id'] = str(course['_id'])
        return courses

    def get_course_by_id(self, id: int) -> Optional[Dict]:
        """Get a course by its ID"""
        course = self.collection.find_one({"id": id})
        if course and '_id' in course:
            course['_id'] = str(course['_id'])
        return course

    def get_course_by_mongo_id(self, mongo_id: str) -> Optional[Dict]:
        """Get a course by its MongoDB _id"""
        try:
            course = self.collection.find_one({"_id": ObjectId(mongo_id)})
            if course and '_id' in course:
                course['_id'] = str(course['_id'])
            return course
        except Exception as e:
            print(f"Error searching for course by MongoDB ID: {str(e)}")
            return None

    def get_courses_by_subject(self, subject_id: int) -> List[Dict]:
        """Get all courses that include a specific subject"""
        courses = list(self.collection.find({"subjects": subject_id}))
        for course in courses:
            if '_id' in course:
                course['_id'] = str(course['_id'])
        return courses 