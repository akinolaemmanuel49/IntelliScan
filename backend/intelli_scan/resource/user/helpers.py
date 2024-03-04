import logging
from typing import Any, Optional, Tuple

from flask import Request, abort

from intelli_scan.database.models.user import UserModel as User


def get_user_by_email(email: str) -> Tuple[bool, Optional[User]]:
    user = User.query.filter_by(email=email).first()
    if user:
        return True, user
    return False, None


def get_user_by_id(user_id) -> Tuple[bool, Optional[User]]:
    user = User.query.filter_by(id=user_id).first()
    if user:
        return True, user
    return False, None


def get_user_details(request: Request):
    user_details = request.get_json()

    if 'email' not in user_details or 'password' not in user_details or 'name' not in user_details:
        logging.warning('Name, email and password fields are required')
        abort(400, 'Email and password fields are required')

    return user_details

def get_user_details_update(request: Request):
    user_details = request.get_json()

    # Check if at least one of the fields to update is provided
    if not any(field in user_details for field in ['email', 'password', 'name']):
        logging.warning('At least one of email, password, or name fields is required for update')
        abort(400, 'At least one of email, password, or name fields is required for update')

    return user_details

