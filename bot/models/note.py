from __future__ import annotations
from pydantic import BaseModel

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Note(BaseModel):
    id: int
    user_id: int
    text: str


class NoteCreate(BaseModel):
    user_id: int
    text: str


class DBNote(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int]
    text: Mapped[str] = mapped_column(Text(), default=False)

    sqlite_autoincrement = True
