#!/usr/bin/env python3
"""This module defines the user table"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """This is user class table"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))  # nullable default to False
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """This method is used for debugging and development"""
        return (f"<User(id={self.id}, email={self.email}, "
                f"hashed_password={self.hashed_password}, "
                f"session_id={self.session_id}, "
                f"reset_token={self.reset_token})>")

    def __str__(self):
        """
        This method return human-readable string representions
        of the objects
        """
        return (f"User(id={self.id}, email={self.email}, "
                f"hashed_password={self.hashed_password}, "
                f"session_id={self.session_id}, "
                f"reset_token={self.reset_token})")
