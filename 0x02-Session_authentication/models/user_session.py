#!/usr/bin/env python3
"""This model imprements storing user sessions"""
from models.base import Base


class UserSession(Base):
    """This classes stores user session ids"""
    def __init__(self, *args: list, **kwargs: dict):
        """This is class constructor method"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
