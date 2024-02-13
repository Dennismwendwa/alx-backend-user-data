#!/usr/bin/env python3
"""This module is for basic authentication"""
from .auth import Auth
from typing import Tuple, TypeVar
import re


class BasicAuth(Auth):
    """This is basic auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """This method extraxts base 63"""
        if isinstance(authorization_header, str):
            pattern = r"Basic (?P<token>.+)"
            all_matches = re.fullmatch(pattern, authorization_header.strip())
            if all_matches is not None:
                return all_matches.group("token")
        return None
