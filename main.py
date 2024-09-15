from fastapi import FastAPI

from routers.users import router as users_router
from routers.store import router as store_router

app = FastAPI()

app.include_router(users_router, prefix='/users')
app.include_router(store_router, prefix='/store')
