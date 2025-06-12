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

    def create_course(self, course_data: Dict) -> Dict:
        """Create a new course in the database"""
        try:
            # Get the next available ID
            last_course = self.collection.find_one(sort=[("id", -1)])
            next_id = 1 if not last_course else last_course["id"] + 1

            # Prepare course data
            course = {
                "id": next_id,
                "name": course_data["name"],
                "subjects": course_data["subjects"]
            }

            # Insert course into database
            result = self.collection.insert_one(course)
            
            # Get the created course
            created_course = self.collection.find_one({"_id": result.inserted_id})
            
            # Convert ObjectId to string for response
            if created_course and '_id' in created_course:
                created_course["_id"] = str(created_course["_id"])
            
            return created_course
        except Exception as e:
            print(f"Error creating course: {str(e)}")
            raise ValueError(f"Failed to create course: {str(e)}")

    def update_course(self, course_id: int, course_data: Dict) -> Optional[Dict]:
        """Update a course by ID"""
        try:
            # Check if course exists
            existing_course = self.get_course_by_id(course_id)
            if not existing_course:
                return None

            # Update course in database
            update_result = self.collection.update_one(
                {"id": course_id},
                {"$set": course_data}
            )

            if update_result.modified_count == 0:
                return None

            # Get updated course
            updated_course = self.get_course_by_id(course_id)
            return updated_course
        except Exception as e:
            print(f"Error updating course: {str(e)}")
            raise ValueError(f"Failed to update course: {str(e)}")

    def delete_course(self, course_id: int) -> bool:
        """Delete a course by ID"""
        try:
            # Check if course exists
            existing_course = self.get_course_by_id(course_id)
            if not existing_course:
                return False

            # Delete course from database
            result = self.collection.delete_one({"id": course_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting course: {str(e)}")
            raise ValueError(f"Failed to delete course: {str(e)}") 