from app.controller.document_controller import DocumentController
from app.models.document import Document, DocumentCreate, DocumentUpdate
from typing import List, Optional

class DocumentService:
    def __init__(self):
        self.controller = DocumentController()

    def get_all_documents(self) -> List[Document]:
        """Get all documents"""
        documents = self.controller.get_all_documents()
        return [Document(**doc) for doc in documents]

    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        """Get a document by ID"""
        document = self.controller.get_document_by_id(document_id)
        return Document(**document) if document else None

    def get_documents_by_type(self, doc_type: str) -> List[Document]:
        """Get all documents of a specific type"""
        documents = self.controller.get_documents_by_type(doc_type)
        return [Document(**doc) for doc in documents]

    def get_documents_by_teacher(self, teacher_id: int) -> List[Document]:
        """Get all documents created by a specific teacher"""
        documents = self.controller.get_documents_by_teacher(teacher_id)
        return [Document(**doc) for doc in documents]

    def get_documents_by_subject(self, subject_id: int) -> List[Document]:
        """Get all documents related to a specific subject"""
        documents = self.controller.get_documents_by_subject(subject_id)
        return [Document(**doc) for doc in documents]

    def get_documents_by_owner(self, owner_id: str) -> List[Document]:
        """Get all documents owned by a specific user"""
        documents = self.controller.get_documents_by_owner(owner_id)
        return [Document(**doc) for doc in documents]

    def create_document(self, document: DocumentCreate) -> Document:
        """Create a new document"""
        try:
            # Convert DocumentCreate to dict for controller
            document_dict = document.model_dump()
            
            # Create document in database
            created_document = self.controller.create_document(document_dict)
            
            # Convert to Document model
            return Document(**created_document)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to create document: {str(e)}")

    def update_document(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        """Update a document"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = {k: v for k, v in document_data.model_dump().items() if v is not None}
            
            if not update_dict:
                raise ValueError("No valid fields to update")

            # Update document in controller
            updated_document = self.controller.update_document(document_id, update_dict)
            
            if not updated_document:
                return None

            # Convert to Document model and return
            return Document(**updated_document)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to update document: {str(e)}")

    def delete_document(self, document_id: int) -> bool:
        """Delete a document"""
        try:
            return self.controller.delete_document(document_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to delete document: {str(e)}")