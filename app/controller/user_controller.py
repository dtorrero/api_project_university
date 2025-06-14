from app.connection.connection import MongoDBConnection
from typing import List, Optional, Dict
from bson import ObjectId

class UserController:
    def __init__(self):
        self.db_connection = MongoDBConnection()
        self.collection = self.db_connection.get_collection('users')

    def get_all_users(self) -> List[dict]:
        """Get all users from the database"""
        users = list(self.collection.find())
        # Convert ObjectId to string for _id field
        for user in users:
            if '_id' in user:
                user['_id'] = str(user['_id'])
        return users

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Get a user by their ID"""
        user = self.collection.find_one({"id": user_id})
        if user and '_id' in user:
            user['_id'] = str(user['_id'])
        return user

    def get_users_by_type(self, user_type: str) -> List[dict]:
        """Get all users of a specific type (teacher/student)"""
        users = list(self.collection.find({"type": user_type}))
        for user in users:
            if '_id' in user:
                user['_id'] = str(user['_id'])
        return users

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get a user by their email (case-insensitive)"""
        # Convert email to lowercase for case-insensitive comparison
        user = self.collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
        if user and '_id' in user:
            user['_id'] = str(user['_id'])
        return user

    def get_next_id(self) -> int:
        """Get the next available user ID"""
        last_user = self.collection.find_one(sort=[("id", -1)])
        return (last_user["id"] + 1) if last_user else 1

    def create_user(self, user_data: Dict) -> dict:
        """Create a new user"""
        # Check if email already exists (case-insensitive)
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            print(f"Email {user_data['email']} already exists in database")
            raise ValueError(f"Email {user_data['email']} already registered")

        # Add ID to user data
        user_data["id"] = self.get_next_id()
        
        # Insert user into database
        result = self.collection.insert_one(user_data)
        
        # Get the created user
        created_user = self.collection.find_one({"_id": result.inserted_id})
        if created_user and '_id' in created_user:
            created_user['_id'] = str(created_user['_id'])
        return created_user

    def update_user(self, user_id: int, user_data: Dict) -> Optional[Dict]:
        """Update a user by ID"""
        try:
            # Check if user exists
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                return None

            # If email is being updated, check if it's already in use
            if "email" in user_data and user_data["email"] != existing_user["email"]:
                email_exists = self.get_user_by_email(user_data["email"])
                if email_exists:
                    raise ValueError(f"Email {user_data['email']} already registered")

            # Update user in database
            update_result = self.collection.update_one(
                {"id": user_id},
                {"$set": user_data}
            )

            if update_result.modified_count == 0:
                return None

            # Get updated user
            updated_user = self.get_user_by_id(user_id)
            return updated_user
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            raise ValueError(f"Failed to update user: {str(e)}")

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        try:
            # Check if user exists
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                return False

            # Delete user from database
            result = self.collection.delete_one({"id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            raise ValueError(f"Failed to delete user: {str(e)}") 