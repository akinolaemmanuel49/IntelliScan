from datetime import datetime

from flask import current_app, make_response, request
from flask_restful import Resource, reqparse

from intelli_scan.database.models.user import UserModel
from utils.authentication.jwt_handler import JWTHandler
from utils.authentication.helper import get_secret_key, get_auth_token, get_allowed_origins


class User(Resource):
    origin = ''

    @staticmethod
    def get_user_details_parsed_args():
        """Parses arguments received from the request.

        Returns:
            A dictionary of the parsed request arguments

        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str,
                            help='Email address used to login. This should be a string',
                            required=True)
        parser.add_argument('name', type=str,
                            help='The name of the user', required=True)
        return parser.parse_args()

    @staticmethod
    def get_user_id_parsed_args():
        """Parses user id arg received from the HTTP request.

        Returns:
            A dictionary of the parsed request argument

        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int,
                            help='The ID for the user', required=True)
        return parser.parse_args()

    @staticmethod
    def get_user_password_parsed_args():
        """Parses user password arg received from the HTTP request.

        Returns:
            A dictionary of the parsed request argument

        """
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str,
                            help='The password for the user', required=True)
        return parser.parse_args()

    @staticmethod
    def check_existing_user(email_address):
        """Returns query object of an existing user or null"""
        return UserModel.query.filter_by(email=email_address).first()

    def options(self):
        response = make_response()
        response.headers['Access-Control-Allow-Credentials'] = True

        # Set Access-Control-Allow-Origin based on request origin
        self.origin = request.headers.get('Origin')
        if self.origin in get_allowed_origins(app=current_app):
            response.headers['Access-Control-Allow-Origin'] = self.origin

        # Set allowed headers and methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

        return response

    def get(self):
        """Returns user details and HTTP status as HTTP response based on HTTP request

        Returns:
            JSON object: A 200 HTTP status and response with details of a user

            JSON object: A 403 HTTP status and response for an unauthenticated or unauthorized user

            JSON object: A 404 HTTP status and response for a non-existing user

        Raises:
            Exception: General exceptions aligned to SQLAlchemy in the form of a 500 HTTP status 
            and JSON content-type response
        """
        data_token = get_auth_token()
        jwt_handler = JWTHandler()

        try:
            # check token validity
            decoded_token_response = jwt_handler.decode(
                encoded_jwt=data_token, secret=get_secret_key(app=current_app))['sub']

            if isinstance(decoded_token_response, int):
                user = UserModel.query.filter_by(
                    id=decoded_token_response).first()

                if user:
                    response = {
                        "user_id": user.id,
                        "name": user.name,
                        "email": user.email
                    }
                    # Get the origin from the request headers
                    self.origin = request.headers.get("Origin")
                    if self.origin in get_allowed_origins(app=current_app):
                        return response, 200, {"Access-Control-Allow-Origin": self.origin}
                    else:
                        return {"message": "Origin not allowed"}, 403
                else:
                    return {"message": "This user does not exist"}, 404
            else:
                return {"message": decoded_token_response}, 403
        except Exception as e:
            return {"message": str(e)}, 500

    def post(self):
        """Registers a new user via HTTP POST request

        Returns:
            JSON object: A 201 HTTP status and response with name of the user that was created

            JSON object: A 400 HTTP status and response for an existing user

        Raises:
            Exception: General exceptions aligned to SQLAlchemy in the form of a 500 HTTP status 
            and JSON content-type response
        """
        data_user_details = self.get_user_details_parsed_args()
        data_password = self.get_user_password_parsed_args()

        try:
            # check if user exists by using email address value
            if not self.check_existing_user(data_user_details['email']):
                user = UserModel(
                    email=data_user_details['email'],
                    name=data_user_details['name'],
                    password_hash=UserModel.generate_hash(
                        data_password['password'])
                )
                user.save_to_db()
                # Get the origin from the request headers
                self.origin = request.headers.get("Origin")
                if self.origin in get_allowed_origins(app=current_app):
                    return {"message": f"User {data_user_details['name']}  was created"}, 201, {"Access-Control-Allow-Origin": f"{self.origin}"}
            else:
                return {"message": "That email address already exists"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def put(self):
        """Updates a user via HTTP PUT request

        Returns:
            JSON object: A 200 HTTP status and response with the of the user that was updated

            JSON object: A 403 HTTP status and response for an unauthenticated or unauthorized user

            JSON object: A 404 HTTP status and response for a non-existing user

        Raises:
            Exception: General exceptions aligned to SQLAlchemy in the form of a 500 HTTP status 
            and JSON content-type response
        """
        data_token = get_auth_token()
        jwt_handler = JWTHandler()

        try:
            # check token validity
            decoded_token_user_id = jwt_handler.decode(
                encoded_jwt=data_token, secret=get_secret_key(app=current_app))['sub']

            if isinstance(decoded_token_user_id, int):
                data_user_details = self.get_user_details_parsed_args()
                data_password = self.get_user_password_parsed_args()

                try:
                    user = UserModel.query.filter_by(
                        id=decoded_token_user_id).first()

                    if user:
                        user.email = data_user_details['email']
                        user.name = data_user_details['name']
                        user.password_hash = UserModel.generate_hash(
                            data_password['password'])
                        user.updated_at = datetime.utcnow()
                        user.save_to_db()
                        # Get the origin from the request headers
                        self.origin = request.headers.get("Origin")
                        if self.origin in get_allowed_origins(app=current_app):
                            return {"message": f"User {data_user_details['name']} was updated"}, 200, {"Access-Control-Allow-Origin": f"{self.origin}"}
                    else:
                        return {"message": "This user does not exist"}, 404
                except Exception as e:
                    return {"message": str(e)}, 500
            else:
                return {"message": "You do not have permission to modify this resource"}, 403
        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self):
        """Deletes a user via HTTP DELETE request

        Returns:
            JSON object: A 200 HTTP status and response with confirmation message of the deletion

            JSON object: A 403 HTTP status and response for an unauthenticated or unauthorized user

            JSON object: A 404 HTTP status and response for a non-existing user

        Raises:
            Exception: General exceptions aligned to SQLAlchemy in the form of a 500 HTTP status 
            and JSON content-type response
        """
        data_token = get_auth_token()
        jwt_handler = JWTHandler()

        try:
            # check token validity
            decoded_token_user_id = jwt_handler.decode(
                encoded_jwt=data_token, secret=get_secret_key(app=current_app))['sub']

            if isinstance(decoded_token_user_id, int):

                try:
                    user = UserModel.query.filter_by(
                        id=decoded_token_user_id).first()

                    if user:
                        user.delete_from_db()
                        # Get the origin from the request headers
                        self.origin = request.headers.get("Origin")
                        if self.origin in get_allowed_origins(app=current_app):
                            return {"message": "The user has been deleted successfully"}, 204, {"Access-Control-Allow-Origin": f"{self.origin}"}
                    else:
                        return {"message": "The user does not exist"}, 404
                except Exception as e:
                    return {"message": str(e)}, 500
            else:
                return {"message": "You do not have permission to modify this resource"}, 403
        except Exception as e:
            return {"message": str(e)}, 500
