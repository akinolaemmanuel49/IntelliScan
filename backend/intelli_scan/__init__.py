from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api


from .database import db
from .endpoints.authentication import Login
from .endpoints.user import User
from .endpoints.inference import Inference


def create_app(config_object: str = 'config.DevelopmentConfig') -> Flask:
    # initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_object)  # load configurations object

    # database initialization
    db.init_app(app)
    migrate = Migrate(app, db)

    # resource routing
    api = Api(app)  # initialize Api instance
    api.add_resource(Login, "/api/login")  # login resource
    api.add_resource(User, "/api/user",
                     "/api/user/<int:user_id>")  # user resource
    api.add_resource(Inference, "/api/inference")  # inference resource

    return app
