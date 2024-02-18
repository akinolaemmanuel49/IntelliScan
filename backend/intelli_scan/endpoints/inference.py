import os

import werkzeug
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app, make_response, request
from flask_restful import Resource, reqparse

from intelli_scan.database.models.user import UserModel
from intelli_scan.database.models.inference import InferenceModel
from utils.authentication.jwt_handler import JWTHandler
from utils.authentication.helper import get_allowed_origins, get_secret_key, get_auth_token


class Inference(Resource):
    origin = ''

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

    def options(self):
        response = make_response()
        response.headers['Access-Control-Allow-Credentials'] = True

        # Set Access-Control-Allow-Origin based on request origin
        self.origin = request.headers.get("Origin")
        if self.origin in get_allowed_origins(app=current_app):
            response.headers['Access-Control-Allow-Origin'] = self.origin

        # Set allowed headers and methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

        return response

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

                            # Create new inference instance in the database
                            inference = InferenceModel(file=new_filename, user_id=user.id)
                            inference.save_to_db()
                            # Get the origin from the request headers
                            self.origin = request.headers.get("Origin")
                            if self.origin in get_allowed_origins(app=current_app):
                                return {'message': 'Upload successful'}, 200, {"Access-Control-Allow-Origin": f"{self.origin}"}
            except Exception as e:
                return {'message': str(e)}, 500
        except Exception:
            return {"message": "You do not have permission to use this resource, re-authenticate"}, 403
        
    def get(self, inference_id=None):
        """Get all inferences belonging to a specific user or get a particular inference using its ID
        
        Args:
            inference_id (int): The ID of the inference to retrieve (default is None)
        
        Returns:
            JSON object: A 200 HTTP status and response with inferences
        
            JSON object: A 403 HTTP status and response for an unauthenticated or unauthorized user
        
            JSON object: A 404 HTTP status and response for a non-existing inference
        
            JSON object: A 500 HTTP status and response for general exceptions
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
                        # Fetch all inferences belonging to the user
                        if inference_id is None:
                            inferences = InferenceModel.query.filter_by(user_id=user.id).all()
                            # Serialize the inferences
                            serialized_inferences = [{
                                "id": inference.id,
                                "file": inference.file,
                                "user_id": inference.user_id,
                                "created_at": str(inference.created_at)
                            } for inference in inferences]
                            return serialized_inferences, 200
                        
                        # Fetch a particular inference using its ID
                        else:
                            inference = InferenceModel.query.filter_by(id=inference_id, user_id=user.id).first()
                            if inference:
                                # Serialize the inference
                                serialized_inference = {
                                    "id": inference.id,
                                    "file": inference.file,
                                    "user_id": inference.user_id,
                                    "created_at": str(inference.created_at)
                                }
                                return serialized_inference, 200
                            else:
                                return {"message": "Inference not found"}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        except Exception:
            return {"message": "You do not have permission to use this resource, re-authenticate"}, 403
