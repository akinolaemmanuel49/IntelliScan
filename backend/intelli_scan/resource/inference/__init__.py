from flask import Blueprint

inference_bp = Blueprint('inference', __name__)

from intelli_scan.resource.inference import routes  # noqa
