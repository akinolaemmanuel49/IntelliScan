import logging
import os
from datetime import datetime

from werkzeug.utils import secure_filename
from flask import current_app

from intelli_scan.resource.inference.errors import InferenceError
from intelli_scan.database.models.user import UserModel as User
from intelli_scan.database.models.inference import InferenceModel as Inference


def infer_action(image, user_id):
    try:
        user: User = User.query.filter_by(id=user_id).first()

        # Secure filename to prevent directory traversal attacks
        filename = secure_filename(image.filename)

        file_extension = filename.rsplit('.', 1)[
            1].lower()

        # Use the configured UPLOAD_FOLDER
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # Ensure the UPLOAD_FOLDER exists
        os.makedirs(upload_folder, exist_ok=True)

        # Create a unique filename using timestamp
        timestamp = datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S")
        new_filename = f'image-{user.id}-{timestamp}.{file_extension}'

        # Save the file to the UPLOAD_FOLDER defined in app.config['UPLOAD_FOLDER']
        file_path = os.path.join(
            upload_folder, new_filename)
        image.save(file_path)

        # Create new inference instance in the database
        inference = Inference(file=new_filename, user_id=user.id)
        inference.save_to_db()
        return True, inference
    except Exception as e:
        logging.error(str(e))
        raise InferenceError('Inference error')
