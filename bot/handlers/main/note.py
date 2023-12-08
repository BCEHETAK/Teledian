from typing import Final

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.filters import states
from bot.keyboards.base import NoteCallback, NotesCallback, note_actions_keyboard, notes_keyboard
from bot.models import DBUser
from bot.models.note import NoteCreate
from bot.services.database.main import Repository
from bot import texts

router: Final[Router] = Router(name=__name__)


@router.message(Command('note'))
async def create_note_command(message: Message, command: CommandObject, user: DBUser, repository: Repository):
    if command.args:
        note = await repository.note.create(NoteCreate(user_id=user.id, text=command.args))
        keyboard = note_actions_keyboard(note.id)
        return message.answer(text=note.text, reply_markup=keyboard)


@router.message(Command(commands=['start', 'notes']))
async def show_notes_command(message: Message, user: DBUser, repository: Repository):
    notes = await repository.note.get_by_user_id(user.id)
    keyboard = notes_keyboard(notes)
    return message.answer(texts.main_menu, reply_markup=keyboard)


@router.callback_query(NotesCallback.filter(F.action == "create"))
async def create_note_callback(query: CallbackQuery, repository: Repository, state: FSMContext):
    await state.set_state(states.CreateNote.begin)
    await query.answer()
    await query.message.edit_text("Пришлите текст заметки")


@router.message(states.CreateNote.begin)
async def create_note_handler(message: Message, user: DBUser, repository: Repository, state: FSMContext):
    if message.text:
        await state.clear()
        note = await repository.note.create(NoteCreate(user_id=user.id, text=message.text))
        keyboard = note_actions_keyboard(note.id)
        return message.answer(text=note.text, reply_markup=keyboard)


@router.callback_query(NotesCallback.filter(F.action == "list"))
async def notes_list_callback(query: CallbackQuery, user: DBUser, repository: Repository):
    notes = await repository.note.get_by_user_id(user.id)
    keyboard = notes_keyboard(notes)
    await query.answer()
    await query.message.edit_text(texts.main_menu, reply_markup=keyboard)


@router.callback_query(NoteCallback.filter(F.action == "show"))
async def show_note_callback(query: CallbackQuery, callback_data: NoteCallback, repository: Repository):
    note = await repository.note.get(callback_data.id)

    if note:
        keyboard = note_actions_keyboard(note.id)
        await query.answer()
        await query.message.edit_text(note.text, reply_markup=keyboard)


@router.callback_query(NoteCallback.filter(F.action == "delete"))
async def delete_note_callback(query: CallbackQuery, callback_data: NoteCallback, 
    user: DBUser, repository: Repository):
    await repository.note.delete(callback_data.id)
    await query.answer(text="Заметка удалена")

    notes = await repository.note.get_by_user_id(user.id)
    keyboard = notes_keyboard(notes)
    await query.message.edit_text(texts.main_menu, reply_markup=keyboard)


@router.callback_query(NoteCallback.filter(F.action == "edit"))
async def edit_note_callback(query: CallbackQuery, callback_data: NoteCallback, 
    repository: Repository, state: FSMContext):
    note = await repository.note.get(callback_data.id)
    await state.set_state(states.EditNote.begin)
    await state.set_data({'note_id': note.id})
    await query.answer()
    await query.message.edit_text("Пришлите новый текст заметки")


@router.message(states.EditNote.begin)
async def edit_note_handler(message: Message, repository: Repository, state: FSMContext):
    if message.text:
        data = await state.get_data()
        await state.clear()
        note_id = data['note_id']
        note = await repository.note.get(note_id)

        if note:
            note.text = message.text
            await repository.note.save(note)

            keyboard = note_actions_keyboard(note.id)
            return message.answer(text=note.text, reply_markup=keyboard)
