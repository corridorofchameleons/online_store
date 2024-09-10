from fastapi import HTTPException
import string

from schemas.users import UserCreateModel


def password_is_valid(password: str, password_2: str) -> bool:
    '''
    Валидатор пароля при регистрации
    '''
    if password != password_2:
        raise HTTPException(status_code=422, detail='Пароли не совпадают')
    if len(password) < 8:
        raise HTTPException(status_code=422, detail='Пароль слишком короткий')
    for sym in password:
        if (sym not in string.digits) and (sym not in string.ascii_letters) and (sym not in '($%&!:)'):
            raise HTTPException(status_code=422, detail='Допустимые символы: a-Z, ($%&!:) и цифры')
    for sym in password:
        if sym in string.ascii_uppercase:
            break
    else:
        raise HTTPException(status_code=422, detail='Пароль должен содержать хотя бы 1 букву в верхнем регистре')
    for sym in password:
        if sym in '($%&!:)':
            break
    else:
        raise HTTPException(status_code=422, detail='Пароль должен содержать хотя бы 1 спецсимвол')

    return True


def phone_is_valid(phone: str) -> bool:
    '''
    Валидатор телефона
    '''
    if phone.startswith('+7') and len(phone) == 12 and phone[2:].isdigit():
        return True
    else:
        raise HTTPException(status_code=422, detail='Телефон должен начинаться с +7 и содержать 10 цифр')


def user_data_is_valid(user: UserCreateModel) -> bool:
    '''
    Главная функция валидации данных при регистрации
    '''
    if password_is_valid(user.password, user.password_2) and phone_is_valid(user.phone):
        return True
