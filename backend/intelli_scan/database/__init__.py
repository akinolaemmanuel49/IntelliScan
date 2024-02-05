from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from config import Config

env = Config()
pwd_context = CryptContext(schemes=env.ENCRYPTION_SCHEMES)

db = SQLAlchemy()
