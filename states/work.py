from aiogram.fsm.state import State, StatesGroup

class AddWork(StatesGroup):
    waiting_position = State()
    waiting_count = State()
    waiting_date = State()

class EditWork(StatesGroup):
    waiting_choice = State()     
    waiting_new_count = State()