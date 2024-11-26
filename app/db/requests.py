import asyncio

from sqlalchemy import select, insert, update, desc, delete

from app.db.models import async_session
from app.db.models import User, UserLocation, Menu, Cart

# Получить все меню
async def get_menu():
    async with async_session() as session:
        return await session.scalars(select(Menu))

# Получить все telegram id
async def get_user_id(user_id):
    async with async_session() as session:
        return await session.scalar(select(User.user_id).where(User.user_id == user_id))

# Получить все меню
async def get_profile(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.user_id == user_id))

# Получить Всю корзину пользователя
async def get_cart(user_id):
    async with async_session() as session:
        return await session.scalars(select(Cart).where(Cart.user_id == user_id))

# Получить Пиццу
async def get_item(menu_id):
    async with async_session() as session:
        return await session.scalar(select(Menu).where(Menu.id == menu_id))

# print(asyncio.run(get_user_id('113546447')))


async def add_user(user_id: int, name: str, contact: str, age: int):
    async with async_session() as session:
        async with session.begin():
            new_user = User(user_id=user_id, name=name, contact=contact, age=age)
            session.add(new_user)

async def add_user_location(user_id: int, location: str):
    async with async_session() as session:
        async with session.begin():
            new_location = UserLocation(user_id=user_id, location=location)
            session.add(new_location)

async def add_menu_item(name: str, picture_id: str, price: int, description: str):
    async with async_session() as session:
        async with session.begin():
            new_menu_item = Menu(name=name, picture_id=picture_id, price=price, description=description)
            session.add(new_menu_item)

async def add_to_cart(menu_id: int, user_id: int, name: str, picture_id: str, price: str):
    async with async_session() as session:
        async with session.begin():
            new_cart_item = Cart(
                menu_id=menu_id,
                user_id=user_id,
                name=name,
                picture_id=picture_id,
                price=price
            )
            session.add(new_cart_item)