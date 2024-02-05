from datetime import datetime
import re

from sqlalchemy.orm import validates

from intelli_scan.database import db, pwd_context


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())

    def save_to_db(self):
        """Writes data to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes data from the database"""
        db.session.delete(self)
        db.session.commit()


class UserModel(BaseModel):
    """Generates the users table"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)

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
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(password: str, password_hash: str) -> bool:
        """Verifies the provided password against the hashed password"""
        return pwd_context.verify(password, password_hash)
