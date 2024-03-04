import logging
from typing import Optional, Tuple

from intelli_scan.resource.user.errors import CreateUserError, DeleteUserError, EmailAlreadyExists, ReadUserError, UpdateUserError, UserNotFound
from intelli_scan.resource.user.helpers import get_user_by_email, get_user_by_id
from intelli_scan.database.models.user import UserModel as User


def create_user_action(user_details) -> Tuple[bool, Optional[User]]:
    try:
        found, _ = get_user_by_email(email=user_details['email'])
        if found:
            logging.warning('That email address already exists')
            raise EmailAlreadyExists('Email address already exists')
        user = User(
            email=user_details['email'],
            name=user_details['name'],
            password_hash=User.generate_hash(user_details['password']))
        user.save_to_db()
        return True, user
    except Exception as e:
        logging.error(str(e))
        raise CreateUserError('Error creating user')


def read_user_action(user_id) -> Tuple[bool, Optional[User]]:
    try:
        found, user = get_user_by_id(user_id=user_id)
        if found:
            return True, user
        logging.warning(f'User with id {user.id} not found')
        raise UserNotFound(f'User with id {user.id} not found')
    except Exception as e:
        logging.error(str(e))
        raise ReadUserError('Error reading user')


def update_user_action(user_id, user_details) -> Tuple[bool, Optional[User]]:
    try:
        found, user = get_user_by_id(user_id=user_id)
        if found:
            user.email = user_details.get('email', user.email)
            user.name = user_details.get('name', user.name)
            user.save_to_db()
            return True, user
        else:
            logging.warning(f'User with id {user_id} not found')
            raise UserNotFound(f'User with id {user_id} not found')
    except Exception as e:
        logging.error(str(e))
        raise UpdateUserError('Error updating user')


def delete_user_action(user_id) -> bool:
    try:
        found, user = get_user_by_id(user_id=user_id)
        if found:
            user.delete_from_db()
            return True
        else:
            logging.warning(f'User with id {user_id} not found')
            raise UserNotFound(f'User with id {user_id} not found')
    except Exception as e:
        logging.error(str(e))
        raise DeleteUserError('Error deleting user')
