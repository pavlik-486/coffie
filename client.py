import asyncio
import datetime
from datetime  import timedelta

import aiohttp
from datetime import time

URL = 'http://127.0.0.1:8000'


async def ragistration_user():
    async with aiohttp.ClientSession() as session:
        add_user = await session.post(f'{URL}/registration',
                                      json={'user_name': 'Sam',
                                            'user_phone': '+79177778890'})

        add_user = await add_user.json()
        print(add_user)


async def add_dish():
    async with aiohttp.ClientSession() as session:
        add_coffie_dish = await session.post(f'{URL}/add_dish', json={'coffie_bar_id': 2,
                                                                          'name': 'Raf',
                                                                          'descriprion': 'Молоко, кофе',
                                                                          'price': 150})
        res = await add_coffie_dish.json()
        print(res)


async def add_c_bar():
    async with aiohttp.ClientSession() as session:
        open_time_str = time(10, 0).strftime('%H:%M')
        close_time_str = time(22, 0).strftime('%H:%M')
        data = {
            'bar_name': 'Сова',
            'open_time': open_time_str,
            'close_time': close_time_str
        }

        await session.post(f'{URL}/add_bar', json=data)


async def all_bars():
    async with aiohttp.ClientSession() as session:
        result = await session.get(f'{URL}/bars')
        list_bars = await result.json()
        print(list_bars)


async def bars_menu():
    async with aiohttp.ClientSession() as session:
        result = await session.get(f'{URL}/bars_menu', params={'bar_name': 'Сова'})
        print(result.url)
        menu = await result.json()
        print(menu)


async def create_order(): # не доделан
    async with aiohttp.ClientSession() as session:


        data = {'user_id': 1,
                'bar_id': 1,
                'coffee_id': 2,
                'create_time': str(datetime.datetime.now().strftime('%Y-%m-%d, %H:%M')),
                'get_order_date': str(datetime.datetime.now() + timedelta(minutes=15))}

        result = await session.post(f'{URL}/create_order', json=data)
        print(1, await result.text())




if __name__ == '__main__':
    asyncio.run(create_order())