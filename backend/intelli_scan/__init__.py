import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from .database import db
from intelli_scan.resource.oauth import register_google_oauth, oauth

jwt = JWTManager()


def create_app(config_object: str = 'config.DevelopmentConfig') -> Flask:
    # initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_object)  # load configurations object

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Database initialization
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)

    oauth.init_app(app=app)
    with app.app_context():
        register_google_oauth()

    # Setup JWT
    jwt.init_app(app)

    # Register blueprints here
    from intelli_scan.resource.authentication import authentication_bp
    from intelli_scan.resource.user import user_bp
    from intelli_scan.resource.inference import inference_bp
    from intelli_scan.resource.oauth import oauth_bp
    app.register_blueprint(authentication_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(inference_bp)
    app.register_blueprint(oauth_bp)

    # Enable CORS for all routes
    CORS(app, supports_credentials=True, expose_headers=[
         "Authorization"])

    return app
