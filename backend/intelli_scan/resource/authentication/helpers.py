import logging
from typing import Dict

from flask import Request, abort


def get_credentials(request: Request) -> Dict[str, str]:
    credentials = request.get_json()

    if 'email' not in credentials or 'password' not in credentials:
        logging.warning('Email and password fields are required')
        abort(400, 'Email and password fields are required')

    return credentials
