#!/usr/bin/env python3
"""This module is for session auth class"""
from flask import request
from models.user import User
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """This is session class"""
    pass
