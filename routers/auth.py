import jwt
from fastapi import HTTPException, APIRouter, status, Request

from config.settings import SECRET_KEY, ALGORITHM
from database.users import get_user_by_email
from schemas.auth import AuthModel
from services.utils import hash_password, create_jwt_token, decode_jwt_token

router = APIRouter()


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
