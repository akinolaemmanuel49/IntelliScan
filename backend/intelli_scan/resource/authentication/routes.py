import logging

from flask import jsonify, request
from flask_jwt_extended import create_access_token

from intelli_scan.resource.authentication import authentication_bp
from intelli_scan.resource.authentication.actions import login_action
from intelli_scan.resource.authentication.helpers import get_credentials


@authentication_bp.route('/api/login', methods=['POST'])
def login():
    data = get_credentials(request=request)
    valid, user = login_action(credentials=data)
    if valid:
        access_token = create_access_token(identity=user.id)
        logging.info('User logged in successfully')
        return jsonify(user_id=user.id, message=f"Logged in as {user.name}", auth_token=access_token)
