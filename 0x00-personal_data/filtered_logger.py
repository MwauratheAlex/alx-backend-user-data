#!/usr/bin/python3
"""filter_datum module"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    returns the log message obfuscated
    args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the log line (message)
    """
    pattern = r''.join(r'(?<={}=)([^{}]+)|'
                       .format(field, separator) for field in fields)
    return re.sub(pattern[:-1], redaction, message)
