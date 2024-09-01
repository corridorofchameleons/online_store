from fastapi.routing import APIRouter

from schemas.users import UserCreateModel, UserOutModel

router = APIRouter()


@router.post('/create', response_model=UserOutModel)
async def create_user(user: UserCreateModel):
    print(user)
    return user
