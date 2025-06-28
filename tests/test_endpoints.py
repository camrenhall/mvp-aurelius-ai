import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4


def test_presign_endpoint_success(client: TestClient, mock_settings):
    """Test successful presign URL generation"""
    with patch('services.s3_service.S3Service.presign_put_url') as mock_presign:
        mock_presign.return_value = "https://test-bucket.s3.amazonaws.com/test-url"
        
        response = client.post("/uploads/presign", json={
            "filename": "test.pdf",
            "profile": "CRE_LEASE"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "doc_id" in data
        assert data["url"] == "https://test-bucket.s3.amazonaws.com/test-url"


def test_presign_endpoint_s3_failure(client: TestClient, mock_settings):
    """Test presign endpoint when S3 service fails"""
    with patch('services.s3_service.S3Service.presign_put_url') as mock_presign:
        mock_presign.return_value = None
        
        response = client.post("/uploads/presign", json={
            "filename": "test.pdf",
            "profile": "CRE_LEASE"
        })
        
        assert response.status_code == 500
        assert "Failed to generate presigned URL" in response.json()["detail"]


def test_callback_endpoint_success(client: TestClient):
    """Test successful document callback"""
    # First create a document
    with patch('services.s3_service.S3Service.presign_put_url') as mock_presign:
        mock_presign.return_value = "https://test-url.com"
        
        presign_response = client.post("/uploads/presign", json={
            "filename": "test.pdf",
            "profile": "CRE_LEASE"
        })
        doc_id = presign_response.json()["doc_id"]
    
    # Then test the callback
    with patch('services.celery_app.process_document.delay') as mock_delay:
        response = client.post(f"/documents/{doc_id}/callback")
        
        assert response.status_code == 200
        assert response.json() == {"queued": True}
        mock_delay.assert_called_once_with(doc_id)


def test_callback_endpoint_not_found(client: TestClient):
    """Test callback endpoint with non-existent document"""
    fake_id = str(uuid4())
    
    response = client.post(f"/documents/{fake_id}/callback")
    
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]