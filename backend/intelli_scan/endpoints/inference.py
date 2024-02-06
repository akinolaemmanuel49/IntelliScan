import os

import werkzeug
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app
from flask_restful import Resource, reqparse

from intelli_scan.database.models.user import UserModel
from utils.authentication.jwt_handler import JWTHandler
from utils.authentication.helper import get_secret_key, get_auth_token


class Inference(Resource):

    @staticmethod
    def get_image_to_infer_parsed_args():
        """Parses arguments received from the request.

        Returns:
            A dictionary of the parsed request arguments

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'picture', type=werkzeug.datastructures.FileStorage, location='files')
        return parser.parse_args()

    def post(self):
        """Upload image via HTTP POST request

        Returns:
            JSON object: A 200 HTTP status and response with confirmation message of the upload

            JSON object: A 403 HTTP status and response for an unauthenticated or unauthorized user

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
            try:
                if isinstance(decoded_token_response, int):
                    user = UserModel.query.filter_by(
                        id=decoded_token_response).first()

                    if user:
                        data_image_to_infer = self.get_image_to_infer_parsed_args()
                        if data_image_to_infer['picture']:
                            original_filename = secure_filename(
                                data_image_to_infer['picture'].filename)
                            file_extension = original_filename.rsplit('.', 1)[
                                1].lower()

                            # Use the configured UPLOAD_FOLDER
                            upload_folder = current_app.config['UPLOAD_FOLDER']

                            # Ensure the UPLOAD_FOLDER exists
                            os.makedirs(upload_folder, exist_ok=True)

                            # Create a unique filename using timestamp
                            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                            new_filename = f'image-{user.id}-{timestamp}.{file_extension}'

                            # Save the file to the UPLOAD_FOLDER
                            file_path = os.path.join(
                                upload_folder, new_filename)
                            data_image_to_infer['picture'].save(file_path)

                            # Update the user's image field in the database
                            user.image = new_filename
                            user.save_to_db()
                            return {'message': 'Upload successful'}, 200
            except Exception as e:
                return {'message': str(e)}, 500
        except Exception:
            return {"message": "You do not have permission to use this resource, re-authenticate"}, 403
