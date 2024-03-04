from flask import Blueprint

user_bp = Blueprint('user', __name__)

from intelli_scan.resource.user import routes  # noqa
