# services/document_service.py
from sqlmodel import Session
from repositories.document_repository import DocumentRepository
from models.document import Document
from services.s3_service import S3Service
from services.celery_app import process_document
from uuid import UUID
from typing import Optional, Tuple

class DocumentService:
    def __init__(self, session: Session):
        self.repository = DocumentRepository(session)
        self.s3_service = S3Service()
    
    def create_document_with_presigned_url(self, filename: str, profile: str) -> Tuple[Document, str]:
        document = Document(filename=filename, profile=profile)
        document = self.repository.create(document)
        
        s3_key = f"documents/{document.id}/{filename}"
        document.s3_key = s3_key
        document = self.repository.update(document)
        
        presigned_url = self.s3_service.presign_put_url(s3_key)
        return document, presigned_url
    
    def trigger_processing(self, doc_id: UUID) -> bool:
        document = self.repository.get_by_id(doc_id)
        if not document:
            return False
        
        process_document.delay(str(doc_id))
        return True
    
    def get_document(self, doc_id: UUID) -> Optional[Document]:
        return self.repository.get_by_id(doc_id)