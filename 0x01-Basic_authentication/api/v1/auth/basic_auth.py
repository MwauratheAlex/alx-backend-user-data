#!/usr/bin/env python3
""" Basic Auth Module"""
from api.v1.auth.auth import Auth


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
