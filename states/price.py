from aiogram.fsm.state import State, StatesGroup

class AddPrice(StatesGroup):
    waiting_title = State()
    waiting_price = State()

class EditPrice(StatesGroup):
    waiting_choice = State()     
    waiting_new_price = State()