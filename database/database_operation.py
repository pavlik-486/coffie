from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from database.Database import session
from database.Database import User, CoffieBar, Menu


async def create_user(name, phone):
    user_name = name
    user_phone = phone
    try:
        if user_phone and user_name:
            user = User(name=user_name, phone=user_phone)
            async with session() as db:
                db.add(user)
                await db.commit()
                return True
    except IntegrityError:
        return False


# черновой вариант, добавить отдельные функции для добавления записей
async def add_dish(coffie_bar_id, coffie_bar_name,
                   name_dish, description, price):
    async with session() as db:
        check_bar = await db.execute(select(CoffieBar.id, CoffieBar.name).where(CoffieBar.id == coffie_bar_id))
        result_check = check_bar.scalar()
        if result_check():
            dish = Menu(coffie_bar_id, name_dish, description, price)
            await db.add(dish)
            await db.commit()
        else:
            coffie_bar = CoffieBar(coffie_bar_name)
            await db.add(coffie_bar)
            await db.commit()