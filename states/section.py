
from aiogram.fsm.state import State, StatesGroup

class UpdateNameSection(StatesGroup):
    waiting_title = State()

class UpdateEmployerSection(StatesGroup):
    waiting_choice = State()     