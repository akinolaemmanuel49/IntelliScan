from typing import List
from flask_restful import reqparse
from flask import Flask


def get_secret_key(app: Flask) -> str:
    return app.config['SECRET_KEY']


def get_auth_token():
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization',
                        location='headers',
                        help='The authentication token in the Authorization header is required to access this resource',
                        required=True)

    args = parser.parse_args()
    auth_header = getattr(args, 'Authorization', None)
    if auth_header and 'Bearer' in auth_header:
        return auth_header.split()[1]
    else:
        raise Exception('Missing or incorrect Authorization header')


def get_allowed_origins(app: Flask) -> List[str]:
    return app.config['ALLOWED_ORIGINS']
