from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Reg
from app.db.requests import get_user_id, get_cart, get_profile, get_item, add_user, add_user_location, add_to_cart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await get_user_id(user_id) == user_id:
        await message.answer(
            'Вы уже зарегистрированы!', reply_markup=kb.main_menu
        )
    else:
        await message.answer(
            '''
            🎉 Добро пожаловать в наш пицца-бот! 🍕

            Рад вас видеть! Здесь вы можете быстро и просто заказать самую вкусную пиццу, не отвлекаясь от важных дел.
            
            Вот как всё работает:
            1️⃣ Выберите любимую пиццу из нашего меню.
            2️⃣ Добавьте ее в корзину.
            3️⃣ Назовите адрес доставки — и всё, мы уже готовим ваш заказ!
            
            💬 Напишите “Зарегистрироваться:”, чтобы сделать заказ.
            
            🔥 Пицца уже ждёт, чтобы согреть ваш день! 😉
            '''
            , reply_markup=kb.register_profile
        )

# @router.message(F.data == 'Зарегистрироваться')
# async def register(message: Message):
#     await message.answer('Выберите: ', reply_markup=kb.main_menu)

# @router.message(Command('reg'))
@router.message(F.text == 'Зарегистрироваться')
async def reg_name(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя:', reply_markup=ReplyKeyboardRemove())

@router.message(Reg.name)
async def reg_contact(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.contact)
    await message.answer('Отправьте контакт:', reply_markup=kb.send_contact)

@router.message(Reg.contact, F.contact)
async def reg_location(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    await state.set_state(Reg.location)
    await message.answer('Отправьте адрес доставки:', reply_markup=kb.send_location)

@router.message(Reg.contact)
async def reg_no_contact(message: Message):
    await message.answer('Отправьте контакт, используя кнопку ниже!')

@router.message(Reg.location, F.location)
async def reg_age(message: Message, state: FSMContext):
    await state.update_data(location=[message.location.latitude, message.location.longitude])
    await state.set_state(Reg.age)
    await message.answer('Отправьте свой возраст', reply_markup=ReplyKeyboardRemove())

@router.message(Reg.location)
async def reg_no_location(message: Message):
    await message.answer('Отправьте локацию через кнопку ниже!')

@router.message(Reg.age)
async def reg_done(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        data = await state.get_data()
        user_id = message.from_user.id
        # dc = {'name': 'Ар', 'contact': '79687200277', 'location': [55.748361, 37.536696], 'age': 32}
        # (user_id: int, name: str, contact: str, age: int):
        # print(dc['name'])
        await add_user(user_id=user_id, name=data['name'], contact=data['contact'], age=data['age'])
        await add_user_location(user_id=user_id, location=str(data['location']))
        # print(data)  # Debugging data output; replace with actual data handling
        # print(user_id)
        await message.answer('Регистрация завершена!', reply_markup=kb.main_menu)
        await state.clear()
    else:
        await message.answer('Отправьте целое число!')

@router.message(F.text == 'Меню')
async def menu(message: Message):
    await message.answer('Добавьте пиццу в корзину:', reply_markup= await kb.menu())


@router.message(F.text == 'Корзина')
async def cart(message: Message):
    user_id = message.from_user.id
    cart_items = await get_cart(user_id=user_id)

    if not cart_items:
        # Если корзина пуста
        await message.answer('Ваша корзина пуста.', reply_markup=kb.cart_user)
    else:
        # Формируем сообщение с содержимым корзины
        cart_content = "\n".join([f"{item.name}: {item.price} руб." for item in cart_items])
        await message.answer(f'В корзине:\n{cart_content}', reply_markup=kb.cart_user)

@router.message(F.text == 'Настройки')
async def cart(message: Message):
    user_id = message.from_user.id
    await message.answer('Выберите пункт:', reply_markup=kb.settings)

@router.message(F.text == 'Назад')
async def cart(message: Message):
    await message.answer('Вернулись в меню', reply_markup=kb.main_menu)

@router.message(F.text == 'Профиль')
async def cart(message: Message):
    user_id = message.from_user.id
    profile = await get_profile(user_id)
    await message.answer(f'''Имя: {profile.name}\nВозраст: {profile.age}\nТелефон: {profile.contact} \n
                            ''', reply_markup=kb.settings) # Адрес доставки: {profile.location} \n

@router.message(F.text == 'Изменить профиль')
async def cart(message: Message):
    user_id = message.from_user.id
    await message.answer('Функционал появится в следующем релизе!', reply_markup=kb.settings)

@router.message(F.text == 'Очистить корзину')
async def cart(message: Message):
    user_id = message.from_user.id
    await message.answer('Функционал появится в следующем релизе!', reply_markup=kb.cart_user)

@router.message(F.text == 'Отправить заказ')
async def cart(message: Message):
    user_id = message.from_user.id
    await message.answer('Заказ отправлен! Функционал появится в следующем релизе!', reply_markup=kb.cart_user)

@router.callback_query(F.data.startswith('pizza_'))
async def add_pizza(callback: CallbackQuery):
    user_id = callback.from_user.id  # Исправлено на callback.from_user.id
    pizza_id = callback.data.split('_')[1]
    menu_o = await get_item(menu_id=pizza_id)
    # print(menu_o) Menu(id=6, name=Овощная, picture_id=img6, price=500, effective_from_dttm=2024-11-18 23:10:16.133076)
    # add_to_cart(menu_id: int, user_id: int, name: str, picture_id: str, price: str):
    await add_to_cart(menu_id=menu_o.id, name=menu_o.name, user_id=user_id, picture_id=menu_o.picture_id,
                      price=menu_o.price)
    await callback.answer()
    await callback.message.edit_text('Пицца добавлена в корзину!')

# @router.message(F.photo)
# async def get_file_id_photo(message: Message):
#     # Получение file_id фотографии
#     file_id = message.photo[-1].file_id  # Берем последнюю (самое большое разрешение)
#     await message.reply(f"Photo file_id: {file_id}")