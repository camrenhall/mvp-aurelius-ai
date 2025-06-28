from uuid import UUID

from models.document import Document


def test_document_creation():
    """Test Document model creation"""
    doc = Document(filename="test.pdf", profile="CRE_LEASE")

    assert doc.filename == "test.pdf"
    assert doc.profile == "CRE_LEASE"
    assert doc.status == "pending"
    assert isinstance(doc.id, UUID)
    assert doc.created_at is not None
    assert doc.updated_at is not None
