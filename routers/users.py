from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from database.users import create_user, delete_user, get_user_by_email, update_user
from models.users import users
from schemas.auth import AuthModel
from schemas.users import UserCreateModel, UserOutModel, UserUpdateModel
from services.services import get_current_user
from services.utils import hash_password, create_jwt_token
from services.validators import user_data_is_valid, phone_is_valid

router = APIRouter()


@router.post('/create', response_model=UserOutModel)
async def register(user: UserCreateModel):
    if user_data_is_valid(user):
        await create_user(user)
        return user


@router.post("/token")
async def login(user: AuthModel):
    """
    Generates token
    """
    found_user = await get_user_by_email(user.email)
    if not found_user:
        raise HTTPException(status_code=404, detail='No user was found')

    hashed_password = hash_password(user.password)
    if found_user.password != hashed_password:
        raise HTTPException(status_code=401, detail='Incorrect email or password')

    access_token = create_jwt_token(data={"email": found_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


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
