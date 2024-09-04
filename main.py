from fastapi import FastAPI, Header, Depends
from config.settings import POSTGRES_HOST
from models.users import users

from routers.users import router as users_router
from routers.auth import router as auth_router, get_current_user
from schemas.users import UserBaseModel

app = FastAPI()

app.include_router(users_router, prefix='/users')
app.include_router(auth_router, prefix='/auth')


@app.get('/main')
async def main(user: users = Depends(get_current_user)):

    print(user)
    return {"status": POSTGRES_HOST}
