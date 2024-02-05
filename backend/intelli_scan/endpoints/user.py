from datetime import datetime
from flask import current_app
from flask_restful import Resource, reqparse

from intelli_scan.database.models.user import UserModel
from utils.authentication.jwt_handler import JWTHandler
from utils.authentication.helper import get_secret_key, get_auth_token


class User(Resource):

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
        parser.add_argument('first_name', type=str,
                            help='The first name of the user', required=True)
        parser.add_argument('last_name', type=str,
                            help='The last name of the user', required=True)
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

    def get(self):
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
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email
                    }
                    return response, 200
                else:
                    return {"message": "This user does not exist"}, 404
            else:
                return {"message": decoded_token_response}, 403
        except Exception as e:
            return {"message": str(e)}, 500

    def post(self):
        data_user_details = self.get_user_details_parsed_args()
        data_password = self.get_user_password_parsed_args()

        try:
            # check if user exists by using email address value
            if not self.check_existing_user(data_user_details['email']):
                user = UserModel(
                    email=data_user_details['email'],
                    first_name=data_user_details['first_name'],
                    last_name=data_user_details['last_name'],
                    password_hash=UserModel.generate_hash(
                        data_password['password'])
                )
                user.save_to_db()
                return {"message": f"User {data_user_details['first_name']} {data_user_details['last_name']} was created"}, 201
            else:
                return {"message": "That email address already exists"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def put(self, user_id):
        data_token = get_auth_token()
        jwt_handler = JWTHandler()
        data_user_id = user_id

        try:
            # check token validity
            decoded_token_user_id = jwt_handler.decode(
                encoded_jwt=data_token, secret=get_secret_key(app=current_app))['sub']

            if int(decoded_token_user_id) == data_user_id:
                data_user_details = self.get_user_details_parsed_args()
                data_password = self.get_user_password_parsed_args()

                try:
                    user = UserModel.query.filter_by(
                        id=data_user_id).first()

                    if user:
                        user.email = data_user_details['email']
                        user.first_name = data_user_details['first_name']
                        user.last_name = data_user_details['last_name']
                        user.password_hash = UserModel.generate_hash(
                            data_password['password'])
                        user.updated_at = datetime.utcnow()
                        user.save_to_db()
                        return {"message": f"User {data_user_details['first_name']} {data_user_details['last_name']} was updated"}, 200
                    else:
                        return {"message": "This user does not exist"}, 404
                except Exception as e:
                    return {"message": str(e)}, 500
            else:
                return {"message": "You do not have permission to modify this resource"}, 403
        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, user_id: int):
        data_token = get_auth_token()
        jwt_handler = JWTHandler()
        data_user_id = user_id

        try:
            # check token validity
            decoded_token_user_id = jwt_handler.decode(
                encoded_jwt=data_token, secret=get_secret_key(app=current_app))['sub']

            if int(decoded_token_user_id) == data_user_id:

                try:
                    user = UserModel.query.filter_by(
                        id=data_user_id).first()

                    if user:
                        user.delete_from_db()
                        return {"message": "This user has been deleted successfully"}, 200
                    else:
                        return {"message": "This user does not exist"}, 404
                except Exception as e:
                    return {"message": str(e)}, 500
            else:
                return {"message": "You do not have permission to modify this resource"}, 403
        except Exception as e:
            return {"message": str(e)}, 500
