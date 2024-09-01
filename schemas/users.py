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


class UserCreateModel(BaseModel):
    """
    Сериализатор модели регистрации
    """
    name: str
    email: str
    phone: str
    password: str
    password_2: str


class UserOutModel(BaseModel):
    """
    Сериализатор модели ответа
    """
    name: str
    email: str
    phone: str
