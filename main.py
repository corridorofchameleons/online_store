from fastapi import FastAPI, Header, Depends
from config.settings import POSTGRES_HOST
from models.users import users

from routers.users import router as users_router
from routers.auth import router as auth_router, get_current_user
from routers.store import router as store_router

app = FastAPI()

app.include_router(users_router, prefix='/users')
app.include_router(auth_router, prefix='/auth')
app.include_router(store_router, prefix='/store')


@app.get('/main')
async def main(user: users = Depends(get_current_user)):

    return {"status": POSTGRES_HOST}
