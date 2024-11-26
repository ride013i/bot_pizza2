from aiogram import types, Router, F
# from app.db.requests import
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from aiogram.filters import Command, Filter

from config import ADMINS
from app.states import AddMenu
from db.requests import add_menu_item

admin = Router()


class AdminProtect(Filter):
    """
    Фильтр для проверки пользователя на админа
    """
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


@admin.message(AdminProtect(), Command('admin'))
async def apanel(message: types.Message):
    await message.answer('''Добро пожаловать в панель Администратора!\nВам доступен следующий функционал:'''
                         , reply_markup=kb.admin_menu)

    # [KeyboardButton(text='Добавить в меню'), KeyboardButton(text='Убрать из меню')],
    # [KeyboardButton(text='Изменить цену'), KeyboardButton(text='Изменить название')],
    # [KeyboardButton(text='Изменить описание'), KeyboardButton(text='Изменить изображение')],
@admin.message(AdminProtect(), F.text == 'Выйти из панели администратора')
async def back_to_menu(message: types.Message):
    await message.answer('''Добро пожаловать в панель Администратора!\nВам доступен следующий функционал:'''
                         , reply_markup=kb.main_menu)
    await message.delete()

@admin.message(AdminProtect(), F.text == 'Добавить в меню')
async def add_name(message: Message, state: FSMContext):
    await state.set_state(AddMenu.name)
    await message.answer('Введите название:', reply_markup=ReplyKeyboardRemove())

@admin.message(AddMenu.name)
async def add_photo(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMenu.picture_id)
    await message.answer('Отправьте картинку:', reply_markup=ReplyKeyboardRemove())

@admin.message(AddMenu.picture_id, F.photo)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(picture_id=message.photo[-1].file_id)
    await state.set_state(AddMenu.description)
    await message.answer('Отправьте описание:', reply_markup=ReplyKeyboardRemove())

@admin.message(AddMenu.description)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddMenu.price)
    await message.answer('Введите цену (только целое число):', reply_markup=ReplyKeyboardRemove())

@admin.message(AddMenu.price)
async def add_done(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=int(message.text))
        data = await state.get_data()
        await add_menu_item(name=data['name'], picture_id=data['picture_id'], price=data['price'],
                            description=data['description'])
        await message.answer('Меню обновили!', reply_markup=kb.admin_menu)
        await state.clear()
    else:
        await message.answer('Отправьте целое число!')

# @admin.message()
# async def unknown(message: types.Message):
#     await message.delete()