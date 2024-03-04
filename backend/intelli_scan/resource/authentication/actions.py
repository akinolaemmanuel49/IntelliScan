import logging
from typing import Optional, Tuple

from intelli_scan.resource.authentication.errors import AuthenticationError, InvalidAuthenticationCredentials
from intelli_scan.database.models.user import UserModel as User


def login_action(credentials) -> Tuple[bool, Optional[User]]:
    try:
        user: User = User.query.filter_by(email=credentials['email']).first()
        if user and User.verify_password(password=credentials['password'], password_hash=user.password_hash):
            return True, user
        raise InvalidAuthenticationCredentials('Invalid credentials')
    except Exception as e:
        logging.error(str(e))
        raise AuthenticationError('Error authenticating user')
