from app.controller.user_controller import UserController
from app.models.user import User, UserCreate, UserUpdate
from typing import List, Optional

class UserService:
    def __init__(self):
        self.controller = UserController()

    def get_all_users(self) -> List[User]:
        """Get all users"""
        users = self.controller.get_all_users()
        return [User(**{**user, "_id": user.get("_id")}) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        user = self.controller.get_user_by_id(user_id)
        return User(**{**user, "_id": user.get("_id")}) if user else None

    def get_users_by_type(self, user_type: str) -> List[User]:
        """Get all users of a specific type"""
        users = self.controller.get_users_by_type(user_type)
        return [User(**{**user, "_id": user.get("_id")}) for user in users]

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            # Convert Pydantic model to dict
            user_dict = user_data.model_dump()
            
            # Create user in controller
            created_user = self.controller.create_user(user_dict)
            
            # Convert to User model and return
            return User(**{**created_user, "_id": created_user.get("_id")})
        except ValueError as e:
            print(f"Validation error while creating user: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            print(f"Unexpected error while creating user: {str(e)}")
            raise Exception(f"Error creating user: {str(e)}")

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update a user"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = {k: v for k, v in user_data.model_dump().items() if v is not None}
            
            if not update_dict:
                raise ValueError("No valid fields to update")

            # Update user in controller
            updated_user = self.controller.update_user(user_id, update_dict)
            
            if not updated_user:
                return None

            # Convert to User model and return
            return User(**{**updated_user, "_id": updated_user.get("_id")})
        except ValueError as e:
            print(f"Validation error while updating user: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            print(f"Unexpected error while updating user: {str(e)}")
            raise Exception(f"Error updating user: {str(e)}")

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        try:
            return self.controller.delete_user(user_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to delete user: {str(e)}") 