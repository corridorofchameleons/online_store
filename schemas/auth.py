from pydantic import BaseModel


class AuthModel(BaseModel):
    '''
    Сериализатор аутентификации
    '''
    email: str
    password: str
