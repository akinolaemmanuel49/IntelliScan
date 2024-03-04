from flask import Blueprint, current_app as app

authentication_bp = Blueprint('authentication', __name__)

from intelli_scan.resource.authentication import routes  # noqa
