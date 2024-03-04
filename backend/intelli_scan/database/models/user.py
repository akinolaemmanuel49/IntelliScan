import re

from sqlalchemy.orm import validates

from intelli_scan.database import db, ph
from intelli_scan.database.models import BaseModel
from intelli_scan.database.models.inference import InferenceModel


class UserModel(BaseModel):
    """Generates the users table"""
    __tablename__ = 'users'

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True, unique=True)
    inferences = db.relationship('InferenceModel', backref='users', lazy=True)

    @validates("email")
    def validate_email(self, key, email):
        if len(email) > 255:
            raise ValueError("Email must be less than 255 characters")
        elif len(email) < 3:
            raise ValueError("Email must be atleast than 2 characters")
        elif not re.match(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Email must be valid")
        else:
            return email

    @staticmethod
    def generate_hash(password: str) -> str:
        """Generates a password hash from a string password"""
        return ph.hash(password=password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifies the provided password against the hashed password"""
        return ph.verify(hash=password_hash, password=password)
