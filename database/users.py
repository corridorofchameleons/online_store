import asyncpg
import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select, insert, delete

from database.db_config import engine
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

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=422, detail=f'User already exists')
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


async def delete_user(user):
    '''
    Удаляет пользователя
    '''
    async with engine.connect() as conn:
        stmt = delete(users).where(users.c.id == user.id)
        await conn.execute(stmt)
        await conn.commit()