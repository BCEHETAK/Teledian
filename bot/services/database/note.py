from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import DBNote
from bot.models.note import NoteCreate

from .base import BaseRepository


class NoteRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, entity=DBNote)

    async def get(self, pk: int) -> DBNote|None:
        return await super().get(pk)

    async def create(self, note: NoteCreate) -> DBNote:
        db_note: DBNote = DBNote(user_id=note.user_id, text=note.text)
        await self.save(db_note)
        return db_note

    async def get_by_user_id(self, user_id: int) -> Sequence[DBNote]:
        notes = await self._session.scalars(select(DBNote).where(DBNote.user_id == user_id))
        return notes.all()
