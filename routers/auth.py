from fastapi import HTTPException, APIRouter

from database.users import get_user_by_email
from schemas.auth import AuthModel
from services.utils import hash_password, create_jwt_token

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
