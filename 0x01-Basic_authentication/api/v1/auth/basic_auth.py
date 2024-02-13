#!/usr/bin/env python3
"""This module is for basic authentication"""
from .auth import Auth
from typing import Tuple, TypeVar
import re
import base64
import binascii
from models.user import User


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """This method decodes strings in base64"""
        if isinstance(base64_authorization_header, str):
            try:
                string = base64.b64decode(base64_authorization_header,
                                          validate=True)
                return string.decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str,
                                 ) -> Tuple[str, str]:
        """This method gets the user credential details"""
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r"(?P<user>[^:]+):(?P<password>.+)"
            full_match = re.fullmatch(
                pattern, decoded_base64_authorization_header.strip()
            )
            if full_match is not None:
                current_user = full_match.group("user")
                user_password = full_match.group("password")
                return current_user, user_password
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """This method constructs user instance from credentials supplied"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                user = User.search({"email": user_email})
            except Exception as e:
                return None
            if len(user) <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Getting the current user from request object"""
        header = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(header)
        string_token = self.decode_base64_authorization_header(b64_token)
        usr_email, usr_password = self.extract_user_credentials(string_token)

        user = self.user_object_from_credentials(usr_email, usr_password)
        print()
        print(user)
        print()
        return user
