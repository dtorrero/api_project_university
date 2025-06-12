from fastapi import APIRouter, HTTPException, status
from app.services.document_service import DocumentService
from app.models.document import Document, DocumentCreate, DocumentUpdate
from typing import List
from pydantic import BaseModel

router = APIRouter()
document_service = DocumentService()

class DeleteResponse(BaseModel):
    message: str

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

@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED, tags=["documents"])
async def create_document(document: DocumentCreate):
    """
    Create a new document with the following information:
    
    - **title**: Document title (1-200 characters)
    - **file_url**: URL or path to the document file
    - **type**: Document type (Lecture Notes, Assignment, Exam, Project, Study Guide)
    - **grade**: Optional grade for the document (0-100)
    - **teacher_id**: ID of the teacher who created the document
    - **subject_id**: ID of the subject the document belongs to
    - **owner**: ID of the user who owns the document (MongoDB ObjectId)
    """
    try:
        return document_service.create_document(document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{document_id}", response_model=Document, tags=["documents"])
async def update_document(document_id: int, document: DocumentUpdate):
    """
    Update a document with the following information:
    
    - **title**: Document title (1-200 characters)
    - **file_url**: URL or path to the document file
    - **type**: Document type (Lecture Notes, Assignment, Exam, Project, Study Guide)
    - **grade**: Optional grade for the document (0-100)
    - **teacher_id**: ID of the teacher who created the document
    - **subject_id**: ID of the subject the document belongs to
    - **owner**: ID of the user who owns the document (MongoDB ObjectId)
    """
    try:
        updated_document = document_service.update_document(document_id, document)
        if not updated_document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found"
            )
        return updated_document
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{document_id}", response_model=DeleteResponse, tags=["documents"])
async def delete_document(document_id: int):
    """Delete a document by ID"""
    try:
        deleted = document_service.delete_document(document_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found"
            )
        return DeleteResponse(message=f"Document with ID {document_id} has been successfully deleted")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 