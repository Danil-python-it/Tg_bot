from aiogram.fsm.state import State, StatesGroup


class getUser(StatesGroup):
    waiting_choice = State()