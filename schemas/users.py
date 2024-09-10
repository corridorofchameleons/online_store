import datetime

from pydantic import BaseModel


class UserBaseModel(BaseModel):
    """
    Сериализатор модели пользователя
    """
    id: int
    name: str
    email: str
    phone: str
    password: str
    registered_at: datetime.datetime


class UserCreateModel(BaseModel):
    """
    Сериализатор модели регистрации
    """
    name: str
    email: str
    phone: str
    password: str
    password_2: str


class UserUpdateModel(BaseModel):
    """
    Сериализатор обновления пользрвателя
    В текущей реализации первичным полем является email,
    поэтому он изменению не подлежит
    """
    name: str
    phone: str


class UserOutModel(BaseModel):
    """
    Сериализатор модели ответа
    """
    name: str
    email: str
    phone: str
