#!/usr/bin/env python3
"""This script hashes password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """This function encrypts passwords"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
