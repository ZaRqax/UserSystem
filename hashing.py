import hashlib

SALT = b'777'


def hash(password):
    """   """
    crypt = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000)
    return str(crypt)[1:]
