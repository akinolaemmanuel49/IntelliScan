from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api


from .database import db
from .endpoints.authentication import GoogleOauthAuth, GoogleOauthSignin, Login, oauth
from .endpoints.user import User
from .endpoints.inference import Inference


def create_app(config_object: str = 'config.DevelopmentConfig') -> Flask:
    # initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_object)  # load configurations object

    # database initialization
    db.init_app(app)
    migrate = Migrate(app, db)

    oauth.init_app(app=app)
    oauth.register(
        name='google',
        server_metadata_url=app.config['GOOGLE_OAUTH2_CONF_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # resource routing
    api = Api(app)  # initialize Api instance
    api.add_resource(Login, "/api/login")  # login resource
    # Google authentication callbacks
    api.add_resource(GoogleOauthSignin, "/api/google/login/callback")
    api.add_resource(GoogleOauthAuth, "/api/google/auth/callback")
    api.add_resource(User, "/api/user",
                     "/api/user/<int:user_id>")  # user resource
    api.add_resource(Inference, "/api/inference")  # inference resource

    return app
