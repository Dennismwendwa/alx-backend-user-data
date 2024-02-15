#!/usr/bin/env python3
"""This module is class auth for all authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class auth for base authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method require"""

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip("/")
            if (excluded_path.endswith("*") and
                    path.startswith(excluded_path[:-1])):
                return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """method authorized"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """method current user"""
        return None

    def session_cookie(self, request=None):
        """gets the session cookie value"""
        if request is not None:
            session_name = os.getenv("SESSION_NAME")
            cookie = request.cookies.get(session_name)
            return cookie
