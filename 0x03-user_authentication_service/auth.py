#!/usr/bin/env python3
"""This is auth module"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """This method hashes passwords"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def _generate_uuid() -> str:
    """This method genereates uuid string"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """This is Auth constructor method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This method register users"""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {existing_user.email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """This method validates password"""
        try:
            existing_user = self._db.find_user_by(email=email)
            hashed_password = existing_user.hashed_password
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """This method creates session for a user"""
        try:
            existing_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            existing_user.session_id = session_id
            self._db.update_user(existing_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
