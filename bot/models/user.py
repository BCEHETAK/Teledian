from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True)
    name: Mapped[str]

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
