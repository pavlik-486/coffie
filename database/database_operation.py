import asyncio

from database.Database import session
from database.Database import User
from sqlalchemy import select

# проверка на наличие пользователя в БД
# async def check(phone):
#     pass
#



async def create_user(data):
    user_name = data.user_name
    user_phone = data.user_phone
    if user_phone and user_name:
        user = User(name=user_name, phone=user_phone)
        async with session() as db:
            db.add(user)
            await db.commit()
    return True
