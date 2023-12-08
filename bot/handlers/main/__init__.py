from typing import Final

from aiogram import Router

from . import note

router: Final[Router] = Router(name=__name__)
router.include_routers(note.router)
