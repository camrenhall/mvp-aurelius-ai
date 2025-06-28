# repositories/document_repository.py
from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from models.document import Document

class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, document: Document) -> Document:
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document
    
    def get_by_id(self, doc_id: UUID) -> Optional[Document]:
        statement = select(Document).where(Document.id == doc_id)
        return self.session.exec(statement).first()
    
    def update(self, document: Document) -> Document:
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document
    
    def list_all(self) -> List[Document]:
        statement = select(Document)
        return list(self.session.exec(statement).all())