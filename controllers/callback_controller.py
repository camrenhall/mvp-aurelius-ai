# controllers/callback_controller.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlmodel import Session

from app import get_session
from services.document_service import DocumentService

router = APIRouter()


class CallbackResponse(BaseModel):
    queued: bool


@router.post("/documents/{doc_id}/callback", response_model=CallbackResponse)
async def document_callback(
    doc_id: UUID = Path(...), session: Session = Depends(get_session)
):
    service = DocumentService(session)
    document = service.get_document(doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    queued = service.trigger_processing(doc_id)
    return CallbackResponse(queued=queued)
