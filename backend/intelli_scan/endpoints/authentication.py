from flask import current_app, make_response, request, url_for
from flask_restful import Resource, reqparse
from authlib.integrations.flask_client import OAuth

from utils.authentication.helper import get_secret_key
from intelli_scan.database.models.user import UserModel
from utils.authentication.jwt_handler import JWTHandler


oauth = OAuth()


class Login(Resource):

    @staticmethod
    def get_login_details_parsed_args():
        """Parses arguments received from the request.

        Returns:
            A dictionary of the parsed request arguments

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, help='The email of the user is required', required=True)
        parser.add_argument(
            'password', type=str, help='The password of the user is required', required=True)
        return parser.parse_args()

    def options(self):
        response = make_response()
        response.headers['Access-Control-Allow-Credentials'] = True

        # Set Access-Control-Allow-Origin based on request origin
        origin = request.headers.get('Origin')
        if origin in ['http://127.0.0.1:5173', 'http://localhost:5173',
                      'http://127.0.0.1:3000', 'http://localhost:3000']:
            response.headers['Access-Control-Allow-Origin'] = origin

        # Set allowed headers and methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

        return response

    def post(self):
        """Returns user details and HTTP status as HTTP response based on HTTP request

        Returns:
            JSON object: A 200 HTTP status and response with details of user id, a message and the authentication token

            JSON object: A 401 HTTP status and response for invalid login credentials

            JSON object: A 404 HTTP status and response for a non-existing user

        Raises:
            Exception: General exceptions aligned to SQLAlchemy in the form of a 500 HTTP status 
            and JSON content-type response
        """
        data = self.get_login_details_parsed_args()

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
                        'message': f"Logged in as {user.name}",
                        'auth_token': auth_token
                    }
                    return response, 200, {"Access-Control-Allow-Origin": "*"}
                else:
                    return {'message': "Wrong user credentials"}, 401
        except Exception as e:
            return {'message': str(e)}, 500


class GoogleOauthSignin(Resource):

    def get(self):
        redirect_uri = url_for('googleoauthauth', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)


class GoogleOauthAuth(Resource):

    def get(self):
        token = oauth.google.authorize_access_token()
        user = UserModel.query.filter_by(
            google_id=token['userinfo']['sub']).first()
        if user:
            jwt_handler = JWTHandler(subject=user.id)
            auth_token = jwt_handler.encode(
                secret=get_secret_key(app=current_app))
            response = {
                'user_id': user.id,
                'message': f"Logged in as {user.name}",
                'auth_token': auth_token
            }
            return response
        check = UserModel.query.filter_by(
            email=token['userinfo']['email']).first()
        if not check:
            user = UserModel(
                email=token['userinfo']['email'],
                name=f"{token['userinfo']['given_name']} {token['userinfo']['family_name']}",
                google_id=token['userinfo']['sub']
            )
            user.save_to_db()
            return {"message": f"User {token['userinfo']['given_name']} {token['userinfo']['family_name']} was created"}, 201, {"Access-Control-Allow-Origin": "*"}
        else:
            return {"message": "That email address already exists"}, 400


class Logout(Resource):

    def post(self):
        pass
