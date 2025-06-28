# controllers/ingest_controller.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app import get_session
from services.document_service import DocumentService

router = APIRouter()


class PresignRequest(BaseModel):
    filename: str
    profile: str


class PresignResponse(BaseModel):
    doc_id: str
    url: str


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/uploads/presign", response_model=PresignResponse)
async def create_presigned_url(
    request: PresignRequest, session: Session = Depends(get_session)
):
    service = DocumentService(session)
    document, presigned_url = service.create_document_with_presigned_url(
        request.filename, request.profile
    )

    if not presigned_url:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL")

    return PresignResponse(doc_id=str(document.id), url=presigned_url)
