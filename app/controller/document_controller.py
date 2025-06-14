from app.connection.connection import MongoDBConnection
from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime

class DocumentController:
    def __init__(self):
        self.db = MongoDBConnection().get_database()
        self.collection = self.db.documents

    def get_all_documents(self) -> List[Dict]:
        """Get all documents from the database"""
        documents = list(self.collection.find())
        print(f"Total documents in database: {len(documents)}")  # Debug print
        # Convert ObjectId to string for _id and owner fields
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'owner' in doc and isinstance(doc['owner'], ObjectId):
                doc['owner'] = str(doc['owner'])
        return documents

    def get_document_by_id(self, id: int) -> Optional[Dict]:
        """Get a document by its ID"""
        document = self.collection.find_one({"id": id})
        if document:
            if '_id' in document:
                document['_id'] = str(document['_id'])
            if 'owner' in document and isinstance(document['owner'], ObjectId):
                document['owner'] = str(document['owner'])
        return document

    def get_documents_by_type(self, type: str) -> List[Dict]:
        """Get all documents of a specific type"""
        documents = list(self.collection.find({"type": type}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'owner' in doc and isinstance(doc['owner'], ObjectId):
                doc['owner'] = str(doc['owner'])
        return documents

    def get_documents_by_teacher(self, teacher_id: int) -> List[Dict]:
        """Get all documents created by a specific teacher"""
        documents = list(self.collection.find({"teacher_id": teacher_id}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'owner' in doc and isinstance(doc['owner'], ObjectId):
                doc['owner'] = str(doc['owner'])
        return documents

    def get_documents_by_subject(self, subject_id: int) -> List[Dict]:
        """Get all documents related to a specific subject"""
        documents = list(self.collection.find({"subject_id": subject_id}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'owner' in doc and isinstance(doc['owner'], ObjectId):
                doc['owner'] = str(doc['owner'])
        return documents

    def get_documents_by_owner(self, owner_id: str) -> List[Dict]:
        """Get all documents owned by a specific user"""
        try:
            print(f"Searching for documents with owner_id: {owner_id}")  # Debug print
            
            # Convert string ID to ObjectId for query
            owner_object_id = ObjectId(owner_id)
            print(f"Converted to ObjectId: {owner_object_id}")  # Debug print
            
            # Search directly in documents collection by owner field
            documents = list(self.collection.find({"owner": owner_object_id}))
            print(f"Found {len(documents)} documents")  # Debug print
            
            # Convert ObjectId to string in response
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
                if 'owner' in doc and isinstance(doc['owner'], ObjectId):
                    doc['owner'] = str(doc['owner'])
            return documents
        except Exception as e:
            print(f"Error searching for documents by owner: {str(e)}")
            return []

    def create_document(self, document_data: Dict) -> Dict:
        """Create a new document in the database"""
        try:
            # Get the next available ID
            last_document = self.collection.find_one(sort=[("id", -1)])
            next_id = 1 if not last_document else last_document["id"] + 1

            # Prepare document data
            document = {
                "id": next_id,
                "title": document_data["title"],
                "file_url": document_data["file_url"],
                "type": document_data["type"],
                "grade": document_data.get("grade"),
                "teacher_id": document_data["teacher_id"],
                "subject_id": document_data["subject_id"],
                "owner": ObjectId(document_data["owner"]),
                "upload_date": datetime.utcnow()
            }

            # Insert document into database
            result = self.collection.insert_one(document)
            
            # Get the created document
            created_document = self.collection.find_one({"_id": result.inserted_id})
            
            # Convert ObjectId to string for response
            if created_document:
                created_document["_id"] = str(created_document["_id"])
                if "owner" in created_document and isinstance(created_document["owner"], ObjectId):
                    created_document["owner"] = str(created_document["owner"])
            
            return created_document
        except Exception as e:
            print(f"Error creating document: {str(e)}")
            raise ValueError(f"Failed to create document: {str(e)}")

    def update_document(self, document_id: int, document_data: Dict) -> Optional[Dict]:
        """Update a document by ID"""
        try:
            # Check if document exists
            existing_document = self.get_document_by_id(document_id)
            if not existing_document:
                return None

            # Convert owner string to ObjectId if it's being updated
            if "owner" in document_data:
                document_data["owner"] = ObjectId(document_data["owner"])

            # Update document in database
            update_result = self.collection.update_one(
                {"id": document_id},
                {"$set": document_data}
            )

            if update_result.modified_count == 0:
                return None

            # Get updated document
            updated_document = self.get_document_by_id(document_id)
            return updated_document
        except Exception as e:
            print(f"Error updating document: {str(e)}")
            raise ValueError(f"Failed to update document: {str(e)}")

    def delete_document(self, document_id: int) -> bool:
        """Delete a document by ID"""
        try:
            # Check if document exists
            existing_document = self.get_document_by_id(document_id)
            if not existing_document:
                return False

            # Delete document from database
            result = self.collection.delete_one({"id": document_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            raise ValueError(f"Failed to delete document: {str(e)}") 