import asyncio

from sqlalchemy.exc import IntegrityError
from database.Database import session
from database.Database import User, Menu, CoffieBar
from sqlalchemy import select


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


async def add_dish(coffie_bar_id,
                   name_dish, description, price):
    async with session() as db:
        check_bar = await db.execute(select(CoffieBar.id, CoffieBar.name).where(CoffieBar.id == coffie_bar_id))
        result_check = check_bar.fetchone()
        check_dish = await db.execute(select(CoffieBar.id, CoffieBar.name, Menu.name).join(Menu).
                                                   where(CoffieBar.id == coffie_bar_id, Menu.name == name_dish))
        result_check_dish = check_dish.fetchone()
        if result_check and not result_check_dish:
            dish = Menu(coffie_bar_id=coffie_bar_id, name=name_dish, description=description, price=price)
            db.add(dish)
            await db.commit()
            return True
        return False


async def add_bar(bar):
    async with session() as db:
        check_bar = await db.execute(select(CoffieBar.id, CoffieBar.name).where(CoffieBar.name == bar))
        result_check = check_bar.fetchone()
        if not result_check:
            bar = CoffieBar(name=bar)
            db.add(bar)
            await db.commit()
            return True
        return False


async def get_all_bars(): # список кофеен
    async with session() as db:
        all_bars = await db.execute(select(CoffieBar.name)) # ЭТО ИТЕРАТОР!!!
        list_bars = all_bars.fetchall()
        list_bars = {i: bar[0] for i, bar in zip(range(1, len(list_bars) + 1), list_bars)}
        return list_bars


async def bars_menu(bar):
    async with session() as db:
        result = await db.execute(select(Menu.name,
                                           Menu.description,
                                           Menu.price).join(CoffieBar).where(CoffieBar.name == bar))
        bar_menu = {bar: {}}

        for index, dish in enumerate(result.fetchall()):
            coffie = {'name': dish[0],
                      'description': dish[1],
                      'price': dish[2]}
            bar_menu[bar][index + 1] = coffie
        return bar_menu




