import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update

from database.db_config import engine, async_session_maker
from models.users import users
from schemas.users import UserBaseModel
from services.utils import hash_password


async def create_user(user):
    '''
    Создает пользователя
    '''
    hashed_password = hash_password(user.password)

    try:
        async with async_session_maker() as session:
            stmt = insert(users).values(
                name=user.name,
                email=user.email,
                phone=user.phone,
                password=hashed_password,
                is_admin=user.is_admin
            )
            await session.execute(stmt)
            await session.commit()

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=422, detail=f'User already exists')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {e}')


async def get_user_by_email(email: str):
    '''
    Ищет пользователя по почте. Возвращает или пользователя, или None
    '''
    async with async_session_maker() as session:
        stmt = select(users).where(users.c.email == email)
        user = await session.execute(stmt)

    return user.first()


async def update_user(user, new_data):
    '''
    Изменяет данные пользователя
    '''
    async with async_session_maker() as session:
        stmt = update(users).returning(users).where(users.c.email == user.email).values(name=new_data.name, phone=new_data.phone)
        try:
            result = await session.execute(stmt)
            upd_user = result.fetchone()._mapping
            await session.commit()
            return UserBaseModel(**upd_user)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=422, detail=f'User already exists')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Internal server error: {e}')


async def delete_user(user):
    '''
    Удаляет пользователя
    '''
    async with async_session_maker() as session:
        stmt = delete(users).where(users.c.id == user.id)
        await session.execute(stmt)
        await session.commit()
