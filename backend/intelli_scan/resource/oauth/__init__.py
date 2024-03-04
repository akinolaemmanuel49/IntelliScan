from flask import Blueprint, current_app as app
from authlib.integrations.flask_client import OAuth

oauth_bp = Blueprint('oauth', __name__)
oauth = OAuth()


def register_google_oauth():
    oauth.register(
        name='google',
        server_metadata_url=app.config['GOOGLE_OAUTH2_CONF_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


from intelli_scan.resource.oauth import routes  # noqa
