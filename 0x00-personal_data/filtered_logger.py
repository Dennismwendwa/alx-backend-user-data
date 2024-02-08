#!/usr/bin/env python3
"""This script returns a log message"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Replacing field value with redaction string"""
    for field in fields:
        message = re.sub(field+"=.*?"+separator,
                         field+"="+redaction+separator, message)
    return message


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
        """This method formats logs"""
        sub_message = super(RedactingFormatter, self).format(record)
        full_message = filter_datum(
            self.fields, self.REDACTION, sub_message, self.SEPARATOR
        )
        return full_message


def get_logger() -> logging.Logger:
    """Create new logger object"""
    logger_ob = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_h = logging.StreamHandler()
    stream_h.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_h)
    return logger_ob


def get_db() -> mysql.connector.connection.MySQLConnection:
    """This function creates a connector to db"""
    DB_HOST = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DB_NAME = os.getenv("PERSONAL_DATA_DB_NAME", "")
    DB_USER = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    BD_PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=3306,
    )
    return connection


def main():
    """This function connects to db and gets dat from users table"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(",")
    query = f"SELECT {fields} FROM users;"
    log_info = get_logger()
    connection = get_db()

    with connection.cursor() as c:
        c.execute(query)
        rows = c.fetchall()
        for r in rows:
            records_data = map(
                lambda k: f"{k[0]}, {k[1]}", zip(columns, r),
            )
            message = f"{'; '.join(list(records_data))}"
            args = ("user_data", logging.INFO, None, None, message,
                    None, None)
            loggs = logging.LogRecord(*args)
            info_logger.handle(loggs)


if __name__ == "__main__":
    main()
