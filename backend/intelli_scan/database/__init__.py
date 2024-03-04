from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher

from config import Config

env = Config()
ph = PasswordHasher()

db = SQLAlchemy()
