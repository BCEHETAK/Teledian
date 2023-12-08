from typing import Iterable

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.models.note import Note


class NotesCallback(CallbackData, prefix="notes"):
    action: str


class NoteCallback(CallbackData, prefix="note"):
    id: int
    action: str


def notes_keyboard(notes: Iterable[Note]):
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
        InlineKeyboardButton(text=note.text, callback_data=NoteCallback(id=note.id, action="show").pack()) 
        for note in notes
        ],
        width=1
    )

    builder.row(InlineKeyboardButton(text="+ Создать заметку", callback_data=NotesCallback(action="create").pack()))

    return builder.as_markup()


def note_actions_keyboard(note_id):
    builder = InlineKeyboardBuilder()

    builder.row(*[
        InlineKeyboardButton(text="Редактировать", callback_data=NoteCallback(id=note_id, action="edit").pack()),
        InlineKeyboardButton(text="Удалить", callback_data=NoteCallback(id=note_id, action="delete").pack()),
        InlineKeyboardButton(text='< Назад', callback_data=NotesCallback(action="list").pack()),
    ], width=1)

    return builder.as_markup()
