#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """ Basic Authentication Class """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ returns the Base64 part of the Authorization header
        for a Basic Authentication:
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        R_base64 = authorization_header.split(' ')[1]
        return R_base64

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ eturns the decoded value of a Base64 string
        base64_authorization_header
        """
        if type(base64_authorization_header) == str:
            try:
                decode_val = base64.b64decode(
                    base64_authorization_header, validate=True)
                return decode_val.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ returns the user email and password
        from the Base64 decoded value """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        userEmail, userPswd = decoded_base64_authorization_header.split(':', 1)
        return userEmail, userPswd

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ returns the User instance based on his email and pswd """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """  retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_val = self.decode_base64_authorization_header(base64_header)
        userEmail, userPswd = self.extract_user_credentials(decoded_val)
        return self.user_object_from_credentials(userEmail, userPswd)
