import asyncio
import aiohttp

URL = 'http://127.0.0.1:8000'


async def ragistration_user():
    async with aiohttp.ClientSession() as session:
        add_user = await session.post(f'{URL}/registration',
                                      json={'user_name': 'Paul', 'user_phone': '+79177778899'})

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



if __name__ == '__main__':
    asyncio.run(add_dish())