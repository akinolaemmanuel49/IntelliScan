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

    auth_token = parser.parse_args()
    return auth_token['Authorization'].split()[1]
