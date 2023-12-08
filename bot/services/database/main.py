from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .user import UserRepository
from .note import NoteRepository


def create_pool(dsn: str) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=dsn)
    return async_sessionmaker(engine, expire_on_commit=False)


class Repository:
    """
    The main repository. Contains all sub-repositories, like for chats, users, etc.
    """

    user: UserRepository
    note: NoteRepository

    __slots__ = ("user", "note")

    def __init__(self, session: AsyncSession) -> None:
        self.user = UserRepository(session=session)
        self.note = NoteRepository(session=session)
