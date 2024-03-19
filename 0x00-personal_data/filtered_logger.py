#!/usr/bin/env python3
"""filter_datum module"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str) -> str:
    """
    returns the log message obfuscated
    args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the log line (message)
    """
    pattern = r'|'.join(r'(?<={}=)([^{}]+)'
                        .format(field, separator) for field in fields)

    return re.sub(pattern, redaction, message)
