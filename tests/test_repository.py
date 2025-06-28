from sqlmodel import Session

from models.document import Document
from repositories.document_repository import DocumentRepository


def test_document_repository_create(session: Session):
    """Test document repository creation"""
    repo = DocumentRepository(session)
    doc = Document(filename="test.pdf", profile="CRE_LEASE")

    created_doc = repo.create(doc)

    assert created_doc.id is not None
    assert created_doc.filename == "test.pdf"
    assert created_doc.profile == "CRE_LEASE"


def test_document_repository_get_by_id(session: Session):
    """Test document repository get by ID"""
    repo = DocumentRepository(session)
    doc = Document(filename="test.pdf", profile="CRE_LEASE")

    created_doc = repo.create(doc)
    retrieved_doc = repo.get_by_id(created_doc.id)

    assert retrieved_doc is not None
    assert retrieved_doc.id == created_doc.id
    assert retrieved_doc.filename == "test.pdf"


def test_document_repository_get_nonexistent(session: Session):
    """Test getting non-existent document returns None"""
    from uuid import uuid4

    repo = DocumentRepository(session)

    result = repo.get_by_id(uuid4())

    assert result is None
