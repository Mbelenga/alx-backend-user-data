#!/usr/bin/env python3
""" Regex-ing """
import re
import logging
from typing import List
import mysql.connector
import os


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message

