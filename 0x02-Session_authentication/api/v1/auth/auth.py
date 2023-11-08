#!/usr/bin/env python3
"""authentication system module"""

from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """Handles authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if path requires auth"""
        if path is None or excluded_paths is None:
            return True

        if len(excluded_paths) == 0:
            return True

        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ validate all requests"""
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        if auth_header:
            return auth_header

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None"""
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
