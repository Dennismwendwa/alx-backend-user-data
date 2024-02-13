#!/usr/bin/env python3
"""This module is class auth for all authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class auth for base authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method require"""
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip("/")
        excluded_paths = [p.rstrip("/") for p in excluded_paths]
        return path not in excluded_paths
        """
        if path is not None and excluded_paths is not None:
            for exc_p in map(lambda k: k.strip(), excluded_paths:
                pattern = ""
                if exc_p[-1] == "*":
                    pattern = f"{exc_p[0:-1]}"
                elif exc_p[-1] == "/":
                    pattern = f"{exc_p[0:-1]}/"
                else:
                    pattern = f"{exc_p}/"

                if re.match(pattern, path):
                    return False
            return true

    def authorization_header(self, request=None) -> str:
        """method authorized"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """method current user"""
        return None
