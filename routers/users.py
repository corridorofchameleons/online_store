from fastapi.routing import APIRouter

from database.users import create_user
from schemas.users import UserCreateModel, UserOutModel

router = APIRouter()


@router.post('/create', response_model=UserOutModel)
async def create(user: UserCreateModel):
    await create_user(user.name, user.email, user.phone, user.password)
    return user
