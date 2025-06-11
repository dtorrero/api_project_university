from app.controller.document_controller import DocumentController
from app.models.document import Document
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