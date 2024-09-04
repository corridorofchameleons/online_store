from hashlib import sha256


def hash_password(password):
    """
    Возвращает захэшированный пароль
    """
    encoded_password = bytes(password, encoding='utf8')
    hashed_password = sha256(encoded_password)
    return hashed_password.hexdigest()
