import sqlalchemy
from fastapi import HTTPException, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session

from database.db_config import engine
from models.users import users
from schemas.users import UserBaseModel
from services.utils import hash_password
from services.validators import password_is_valid, phone_is_valid


async def create_user(user):
    '''
    Создает пользователя
    '''
    hashed_password = hash_password(user.password)

    try:
        async with engine.connect() as conn:
            stmt = insert(users).values(
                name=user.name,
                email=user.email,
                phone=user.phone,
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


async def update_user(user, new_data):
    '''
    Изменяет данные пользователя
    '''
    async with engine.connect() as conn:
        stmt = update(users).returning(users).where(users.c.email == user.email).values(name=new_data.name, phone=new_data.phone)
        try:
            result = await conn.execute(stmt)
            upd_user = result.fetchone()._mapping
            await conn.commit()
            return UserBaseModel(**upd_user)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=422, detail=f'User already exists')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Internal server error: {e}')


async def delete_user(user):
    '''
    Удаляет пользователя
    '''
    async with engine.connect() as conn:
        stmt = delete(users).where(users.c.id == user.id)
        await conn.execute(stmt)
        await conn.commit()
