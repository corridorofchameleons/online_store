from hashlib import sha256

import jwt

from config.settings import SECRET_KEY, ALGORITHM


def hash_password(password):
    """
    Возвращает захэшированный пароль
    """
    encoded_password = bytes(password, encoding='utf8')
    hashed_password = sha256(encoded_password)
    return hashed_password.hexdigest()


def create_jwt_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])