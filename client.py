import asyncio
import aiohttp

URL = 'http://127.0.0.1:8000'


async def main():
    async with aiohttp.ClientSession() as session:
        result = await session.post(f'{URL}/registration', json={'user_name': 'Sam',
                                                 'user_phone': '+79157889900'})
        res = await result.json()
        print(res)


if __name__ == '__main__':
    asyncio.run(main())