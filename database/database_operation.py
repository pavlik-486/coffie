from sqlalchemy.exc import IntegrityError

from database.Database import session, Order
from database.Database import User, Menu, CoffieBar
from sqlalchemy import select, update, func, between, and_


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
        bar = await db.execute(select(CoffieBar.id, CoffieBar.name).where(CoffieBar.id == coffie_bar_id))
        result_bar = bar.fetchone()
        check_dish = await db.execute(select(CoffieBar.id, CoffieBar.name, Menu.name).join(Menu).
                                                   where(CoffieBar.id == coffie_bar_id, Menu.name == name_dish))
        result_check_dish = check_dish.fetchone()
        if result_bar and not result_check_dish:
            dish = Menu(coffie_bar_id=coffie_bar_id, name=name_dish, description=description, price=price)
            db.add(dish)
            await db.commit()
            return True
        return False


async def add_bar(bar_name, open, close): # добавление новой кофейни
    async with session() as db:
        bar = await db.execute(select(CoffieBar.id, CoffieBar.name).where(CoffieBar.name == bar_name))
        result_bar = bar.fetchone()
        if not result_bar:
            bar = CoffieBar(name=bar_name, open_time=open, close_time=close)
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
        if len(bar_menu) != 0:
            return bar_menu
        return f'bar {bar} is not found'


async def create_order(user_id, bar, coffie_id, create_date, get_order_date): # не доделан
    async with session() as db:
        get_user = await db.execute(select(User.name, User.phone).where(User.id == user_id))
        user = get_user.fetchall()
        # Сделать шаг для выбора времени получения заказа
        # сделать обработку времени получения
        if user:
            order = Order(user_id=user_id, coffie_bar_id=bar, dish_id=coffie_id,
                          create_time=create_date, get_order_time=get_order_date)
            db.add(order)
            await db.commit()
            return {'successfully': f'order for {user_id} have been created'}
        return {'error': f'order with {user_id} not found'}


async def change_status(order_id, new_status):
    async with session() as db:
        await db.execute(update(Order).where(Order.id == order_id).values({'status': new_status}))
        await db.commit()
        return True


async def get_statistic(bar, start_time=None, end_time=None, weekday=None):
    async with session() as db:
        if start_time and end_time:
            stat = select(
                            CoffieBar.name,
                            func.sum(Menu.price).label('total_sum'),
                            func.count(Order.id).label('orders_count')
                        ).select_from(
                            CoffieBar
                        ).join(
                            Menu, CoffieBar.id == Menu.coffie_bar_id
                        ).join(
                            Order, CoffieBar.id == Order.coffie_bar_id
                        ).where(
                            and_(
                                CoffieBar.name == bar,
                                Order.create_time.between(start_time, end_time),
                                Order.status == 'Completed'
                            )
                        ).group_by(
                            CoffieBar.name
                        )
            result = await db.execute(stat)
            return result.fetchall()
        # не запускал еще, также дописать статистику по дням

