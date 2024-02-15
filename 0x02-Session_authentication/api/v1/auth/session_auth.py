#!/usr/bin/env python3
"""This module is for session auth class"""
from flask import request
from models.user import User
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """This is session class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """This method creates user session id"""
        if isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """This method takes session id and returns the user id"""
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """This method gets the current user from the session"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """This method destoy sessions' instances"""
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        if ((request is None or session_id is None) or
                user is None):
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_d]
        return True
