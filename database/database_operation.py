from database.Database import session
from database.Database import User

async def create_user(data):
    user_name = data.user_name
    user_phone = data.user_phone
    user = User(user_name, user_phone)
    async with session as db:
        db.add(user)
        await db.commit()

