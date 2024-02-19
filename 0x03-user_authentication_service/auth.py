#!/usr/bin/env python3
"""Module contains auth helper functions"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
