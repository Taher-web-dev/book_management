from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def verify_password(hash, password):
    return ph.verify(hash, password)
