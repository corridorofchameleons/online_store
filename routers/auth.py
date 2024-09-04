import jwt
from fastapi import HTTPException, APIRouter, status, Request

from config.settings import SECRET_KEY, ALGORITHM
from database.users import get_user_by_email
from schemas.users import UserAuth
from services.utils import hash_password

router = APIRouter()


def create_jwt_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login(user: UserAuth):
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


def decode_jwt_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(request: Request):
    """
    Получает текущего пользователя, если он есть
    """
    try:
        token = request.headers.get('Authorization').split()[1]
        found_user = decode_jwt_token(token)
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError, IndexError):
        raise HTTPException(status_code=401, detail='Authentication failed')

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_email(found_user.get('email'))

    if not user:
        raise HTTPException(status_code=401, detail='Wrong token')

    return user
