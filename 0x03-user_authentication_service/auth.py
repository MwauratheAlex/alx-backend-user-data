#!/usr/bin/env python3
"""Module contains auth helper functions"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a random uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf8')
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf8'),
                user.hashed_password.encode('utf8')
            )
        except Exception:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Creates a session for user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Get user from session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> Optional[str]:
        """Return user password reset token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user password and set reset_token to None"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode("utf8")
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError()
