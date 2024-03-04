import logging

from flask import Request, abort


def get_image(request: Request):
    # Check if the request contains a file named 'picture'
    if 'picture' not in request.files:
        logging.warning('No picture file provided')
        abort(400, 'No picture file provided')

    # Get the file object for the 'picture' field
    image_file = request.files['picture']

    # Check if a file is selected
    if image_file.filename == '':
        logging.warning('No selected image file')
        abort(400, 'No selected image file')

    return image_file
