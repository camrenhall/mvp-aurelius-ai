# models/document.py
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
    profile: str
    status: str = "pending"
    s3_key: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
