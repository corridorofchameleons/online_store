from fastapi import HTTPException
from sqlalchemy import select, insert

from database.db_config import engine, get_async_session
from models.users import users
from services.utils import hash_password


async def create_user(name, email, phone, password):
    '''
    Создает пользователя
    '''
    hashed_password = hash_password(password)

    try:
        async with engine.connect() as conn:
            stmt = insert(users).values(
                name=name,
                email=email,
                phone=phone,
                password=hashed_password
            )
            await conn.execute(stmt)
            await conn.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {e}')


async def get_user_by_email(email: str):
    '''
    Ищет пользователя по почте. Возвращает или пользователя, или None
    '''
    async with engine.connect() as conn:
        stmt = select(users).where(users.c.email == email)
        user = await conn.execute(stmt)

    return user.first()
