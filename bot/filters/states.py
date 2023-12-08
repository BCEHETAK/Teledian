from typing import Final

from aiogram.filters import Filter, StateFilter
from aiogram.fsm.state import State, StatesGroup


class SGForm(StatesGroup):
    name = State()
    age = State()


class CreateNote(StatesGroup):
    begin = State()


class EditNote(StatesGroup):
    begin = State()


NoneState: Final[Filter] = StateFilter(None)
AnyState: Final[Filter] = ~NoneState
