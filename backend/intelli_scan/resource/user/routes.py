import logging

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from intelli_scan.resource.user.errors import EmailAlreadyExists, UserNotFound
from intelli_scan.resource.user import user_bp
from intelli_scan.resource.user.actions import create_user_action, delete_user_action, read_user_action, update_user_action
from intelli_scan.resource.user.helpers import get_user_details, get_user_details_update


@user_bp.route('/api/user', methods=['POST'], endpoint='create-user')
def create_user():
    try:
        data = get_user_details(request=request)
        created, user = create_user_action(user_details=data)
        if created:
            logging.info(f"User {user.name} was created")
            return jsonify(message=f"User {user.name} was created"), 201
    except EmailAlreadyExists:
        return jsonify(message='Email address already exists'), 400
    except Exception as e:
        return jsonify(message=f'Error: {str(e)}'), 500


@user_bp.route('/api/user', methods=['GET'], endpoint='read-user')
@jwt_required()
def read_user():
    try:
        user_id = get_jwt_identity()
        found, user = read_user_action(user_id=user_id)
        if found:
            logging.info(f'Found user with id {user.id}')
            return jsonify(user_id=user.id, name=user.name, email=user.email)
    except UserNotFound:
        return jsonify(message='User not found'), 404
    except Exception as e:
        return jsonify(message=f'Error: {str(e)}'), 500


@user_bp.route('/api/user', methods=['PUT'], endpoint='update-user')
@jwt_required()
def update_user():
    try:
        data = get_user_details_update(request=request)
        user_id = get_jwt_identity()

        updated, user = update_user_action(user_details=data, user_id=user_id)
        if updated:
            logging.info(f"User with id {user.id} was updated")
            return jsonify(message=f"User with id {user.id} was updated"), 200
    except UserNotFound:
        return jsonify(message='User not found'), 404
    except Exception as e:
        return jsonify(message=f'Error: {str(e)}'), 500


@user_bp.route('/api/user', methods=['DELETE'], endpoint='delete-user')
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()

        deleted = delete_user_action(user_id=user_id)
        if deleted:
            logging.info(f"User with id {user_id} was deleted")
            return jsonify(message=f"User with id {user_id} was deleted"), 200
    except UserNotFound:
        return jsonify(message='User not found'), 404
    except Exception as e:
        return jsonify(message=f'Error: {str(e)}'), 500
