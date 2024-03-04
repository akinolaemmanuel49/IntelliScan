import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    # load dot env file
    env_path = Path("..") / ".env"
    load_dotenv(dotenv_path=env_path)

    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = eval(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    )
    SQLALCHEMY_ECHO: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL").replace('postgres', 'postgresql', 1)
    ENCRYPTION_SCHEMES: list[str] = ["bcrypt"]
    GOOGLE_OAUTH2_CONF_URL: str = os.environ.get('GOOGLE_OAUTH2_CONF_URL')
    GOOGLE_CLIENT_ID: str = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.environ.get('GOOGLE_CLIENT_SECRET')
    UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER')
    ALLOWED_ORIGINS: list = [str(origin) for origin in str(
        os.environ.get('ALLOWED_ORIGINS')).split(' ')]


class ProductionConfig(Config):
    SQLALCHEMY_ECHO: bool = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
