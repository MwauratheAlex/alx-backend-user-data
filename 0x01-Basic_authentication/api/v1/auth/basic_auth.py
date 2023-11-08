#!/usr/bin/env python3
""" Basic Auth Module"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Implements basic authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extracts base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None

        header_values = authorization_header.split(' ')

        if header_values[0] != 'Basic':
            return None

        return (header_values[1] if len(header_values) == 2 else None)

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes base64 authoriztion header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            return message_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user credentials from
        decoded_base64_authorization_header"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        cred_1, cred_2 = decoded_base64_authorization_header.split(':')

        return cred_1, cred_2

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns a user object extracted using credentials:"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            user = User.search({'email': user_email})
        except Exception:
            return None

        if not user:
            return None

        if user[0].is_valid_password(user_pwd):
            return user[0]

        return None
