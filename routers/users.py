from fastapi import Depends
from fastapi.routing import APIRouter

from database.users import create_user, delete_user, get_user_by_email, update_user
from models.users import users
from schemas.users import UserCreateModel, UserOutModel, UserUpdateModel
from services.services import get_current_user
from services.validators import user_data_is_valid, phone_is_valid

router = APIRouter()


@router.post('/create', response_model=UserOutModel)
async def create(user: UserCreateModel):
    if user_data_is_valid(user):
        await create_user(user)
        return user


@router.delete('/delete', response_model=UserOutModel)
async def delete(user: users = Depends(get_current_user)):
    await delete_user(user)
    return user


@router.get('/me', response_model=UserOutModel)
async def get(user: users = Depends(get_current_user)):
    await get_user_by_email(user.email)
    return user


@router.put('/update', response_model=UserOutModel)
async def put(new_data: UserUpdateModel, user: users = Depends(get_current_user)):
    if phone_is_valid(new_data.phone):
        upd_user = await update_user(user, new_data)
        return upd_user
