import logging
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from intelli_scan.resource.user.errors import UserNotFound
from intelli_scan.resource.inference import inference_bp
from intelli_scan.resource.inference.helpers import get_image
from intelli_scan.resource.inference.actions import infer_action


@inference_bp.route('/api/inference', methods=['POST'], endpoint='infer')
@jwt_required()
def infer():
    try:
        user_id = get_jwt_identity()
        data = get_image(request=request)
        inferred, inference = infer_action(image=data, user_id=user_id)
        if inferred:
            logging.info("Inference was generated from image")
    except UserNotFound:
        return jsonify(message='User not found'), 404
    except Exception as e:
        return jsonify(message=f'Error: {str(e)}'), 500
