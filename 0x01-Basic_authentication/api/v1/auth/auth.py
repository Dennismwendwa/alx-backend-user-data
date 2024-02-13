#!/usr/bin/env python3
"""This module is class auth for all authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class auth for base authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method require"""
        return False

    def authorization_header(self, request=None) -> str:
        """method authorized"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """method current user"""
        return None
