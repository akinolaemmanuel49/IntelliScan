import logging
from typing import List

from flask import Flask
from email_validator import validate_email, EmailNotValidError


def get_secret_key(app: Flask) -> str:
    return app.config['SECRET_KEY']


# def is_valid_email(email: str) -> bool:
#     try:
#         # Validate the email address
#         v = validate_email(email)
#         # Replace with the normalized form (lowercase domain, etc.)
#         email = v["email"]
#         return True
#     except EmailNotValidError as e:
#         logging.error(str(e))
#         return False


def get_allowed_origins(app: Flask) -> List[str]:
    return app.config['ALLOWED_ORIGINS']
