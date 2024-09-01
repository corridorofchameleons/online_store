from fastapi import FastAPI

import routers
from config.settings import POSTGRES_HOST

from routers.users import router as users_router
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(users_router, prefix='/users')
app.include_router(auth_router, prefix='/auth')


@app.get('/main')
async def main():
    return {"status": POSTGRES_HOST}
