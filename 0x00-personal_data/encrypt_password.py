#!/usr/bin/env python3
"""Password hashing module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password and returns hashed password"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password"""
    pwd_bytes = password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_password)
