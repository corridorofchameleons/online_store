import jwt
from fastapi import HTTPException, status, Request

from database.users import get_user_by_email
from schemas.store import CartItemListModel
from services.utils import decode_jwt_token


async def get_current_user(request: Request):
    """
    Получает текущего пользователя, если он есть
    """
    try:
        token = request.headers.get('Authorization').split()[1]
        found_user = decode_jwt_token(token)
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError, IndexError, AttributeError):
        raise HTTPException(status_code=401, detail='Authentication failed')

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = await get_user_by_email(found_user.get('email'))

    if not user:
        raise HTTPException(status_code=401, detail='Wrong token')

    return user


async def user_is_admin(request: Request):
    """
    Проверяет, является ли пользователь админом
    """
    user = await get_current_user(request)
    if not user.is_admin:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user
