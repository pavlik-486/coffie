import asyncio
import aiohttp

URL = 'http://127.0.0.1:8000'


async def ragistration_user():
    async with aiohttp.ClientSession() as session:
        add_user = await session.post(f'{URL}/registration',
                                      json={'user_name': 'Paul',
                                            'user_phone': '+79177778899'})

        add_user = await add_user.json()
        print(add_user)


async def add_dish():
    async with aiohttp.ClientSession() as session:
        add_coffie_dish = await session.post(f'{URL}/add_dish', json={'coffie_bar_id': 1,
                                                                          'name': 'Mokka',
                                                                          'descriprion': 'Молоко, кофе',
                                                                          'price': 150})
        res = await add_coffie_dish.json()
        print(res)


async def add_c_bar():
    async with aiohttp.ClientSession() as session:
        add_bar_c = await session.post(f'{URL}/add_bar', json={'bar_name': 'Surf'})
        res = await add_bar_c.json()
        print(res)


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



if __name__ == '__main__':
    asyncio.run(bars_menu())