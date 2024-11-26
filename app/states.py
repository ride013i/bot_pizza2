from aiogram.fsm.state import State, StatesGroup

class Reg(StatesGroup):
    name = State()
    contact = State()
    location = State()
    age = State()
    photo = State()

class AddMenu(StatesGroup):
    name = State()
    picture_id = State()
    price = State()
    description = State()

