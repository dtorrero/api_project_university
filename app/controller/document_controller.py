from app.connection.connection import MongoDBConnection
from typing import List, Optional, Dict
from bson import ObjectId

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