from fastapi import Depends
from fastapi.routing import APIRouter

from database.users import create_user, delete_user
from models.users import users
from routers.auth import get_current_user
from schemas.users import UserCreateModel, UserOutModel

router = APIRouter()


@router.post('/create', response_model=UserOutModel)
async def create(user: UserCreateModel):
    await create_user(user.name, user.email, user.phone, user.password)
    return user


@router.delete('/delete', response_model=UserOutModel)
async def delete(user: users = Depends(get_current_user)):
    await delete_user(user)
    return user
