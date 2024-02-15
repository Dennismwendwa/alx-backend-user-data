#!/usr/bin/env python3
"""This module implements session id storage"""
from flask import request
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """This is class session DB auth"""
    def create_session(self, user_id=None) -> str:
        """This method creates new session"""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            dic = {
                "user_id": user_id,
                "session_id": session_id,
            }
            u_session = UserSession(**dic)
            u_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """This method gets the user form session id"""
        try:
            session = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if len(session) <= 0:
            return None

        current_time = datetime.now()
        time = timedelta(seconds=self.session_duration)
        last_time = session[0].created_at + time

        if last_time < current_time:
           return None

        return session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """This method deletes user from session"""
        session_id = self.session_cookie(request)
        try:
            session = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if len(session) <= 0:
            return False

        session[0].remove()
        return True
