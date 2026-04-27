import asyncio
import aiohttp

URL = 'http://127.0.0.1:8000'


async def main():
    async with aiohttp.ClientSession() as session:
        add_user = await session.post(f'{URL}/registration', json={'user_name': 'Sam'})
        add_user = await add_user.json()
        print(add_user)







if __name__ == '__main__':
    asyncio.run(main())