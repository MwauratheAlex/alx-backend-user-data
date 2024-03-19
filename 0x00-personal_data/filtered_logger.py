#!/usr/bin/env python3
"""filter_datum module"""
import os
import re
from typing import List
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """Creates and returns a logging.Logger object"""
    logger = logging.getLogger(name="user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database"""
    db_config = {
        "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        "port": 3306,
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        "database": os.getenv("PERSONAL_DATA_DB_NAME"),
    }
    return mysql.connector.connect(**db_config)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
