import asyncio

from sqlalchemy import select, insert

from database.db_config import engine
from models.users import users


async def create_user(name, email, phone, password):
    async with engine.connect() as conn:
        stmt = insert(users).values(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        await conn.execute(stmt)
        await conn.commit()


asyncio.run(create_user('1', '2', '3', '4'))