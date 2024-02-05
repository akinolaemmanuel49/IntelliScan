from flask import current_app
from flask_restful import Resource, reqparse

from utils.authentication.helper import get_secret_key
from intelli_scan.database.models.user import UserModel
from utils.authentication.jwt_handler import JWTHandler


class Login(Resource):

    @staticmethod
    def get_login_details():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, help='The email of the user is required', required=True)
        parser.add_argument(
            'password', type=str, help='The password of the user is required', required=True)
        return parser.parse_args()

    def post(self):
        data = self.get_login_details()

        try:
            user = UserModel.query.filter_by(email=data['email']).first()

            # return 404 response if a user with that email does not exist
            if not user:
                return {'message': "This user does not exist"}, 404
            else:
                # get authentication token
                jwt_handler = JWTHandler(subject=user.id)
                auth_token = jwt_handler.encode(
                    secret=get_secret_key(app=current_app))

                # verify password and return 401 response if it fails to verify
                if UserModel.verify_hash(data['password'], user.password_hash):
                    response = {
                        'user_id': user.id,
                        'message': f"Logged in as {user.first_name} {user.last_name}",
                        'auth_token': auth_token
                    }
                    return response, 200
                else:
                    return {'message': "Wrong user credentials"}, 401
        except Exception as e:
            return {'message': str(e)}, 500


class Logout(Resource):

    def post(self):
        pass
