from fastapi import APIRouter, HTTPException, status
from app.services.document_service import DocumentService
from app.models.document import Document
from typing import List

router = APIRouter()
document_service = DocumentService()

@router.get("/", response_model=List[Document])
async def get_documents():
    """Get all documents"""
    return document_service.get_all_documents()

@router.get("/{id}", response_model=Document)
async def get_document(id: int):
    """Get a document by its ID"""
    document = document_service.get_document_by_id(id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {id} not found"
        )
    return document

@router.get("/type/{doc_type}", response_model=List[Document])
async def get_documents_by_type(doc_type: str):
    """Get all documents of a specific type"""
    valid_types = ['Lecture Notes', 'Assignment', 'Exam', 'Project', 'Study Guide']
    if doc_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Document type must be one of: {', '.join(valid_types)}"
        )
    return document_service.get_documents_by_type(doc_type)

@router.get("/teacher/{teacher_id}", response_model=List[Document])
async def get_documents_by_teacher(teacher_id: int):
    """Get all documents created by a specific teacher"""
    return document_service.get_documents_by_teacher(teacher_id)

@router.get("/subject/{subject_id}", response_model=List[Document])
async def get_documents_by_subject(subject_id: int):
    """Get all documents related to a specific subject"""
    return document_service.get_documents_by_subject(subject_id)

@router.get("/owner/{owner_id}", response_model=List[Document])
async def get_documents_by_owner(owner_id: str):
    """Get all documents owned by a specific user"""
    return document_service.get_documents_by_owner(owner_id) 