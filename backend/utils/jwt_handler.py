from typing import Any
import jwt
from datetime import datetime, timedelta


class JWTHandler:
    def __init__(self, subject: str, expires_after: float, **kwargs) -> None:
        current_time = datetime.utcnow()
        expiration_time = current_time + timedelta(hours=expires_after)

        self.payload = {
            "sub": subject,
            "iat": current_time.timestamp(),
            "exp": expiration_time.timestamp()
        }

        for k, v in kwargs.items():
            self.payload[k] = v

    def encode(self, secret: str = '', algorithm='HS256') -> str:
        try:
            return jwt.encode(payload=self.payload, key=secret, algorithm=algorithm)
        except Exception as e:
            return str(e)

    @staticmethod
    def decode(encoded_jwt: str, secret: str = '', algorithm='HS256') -> dict[str, Any]:
        try:
            payload = jwt.decode(
                jwt=encoded_jwt, key=secret, algorithms=algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again"
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again"

    # DEBUG
    def __repr__(self) -> str:
        result = ''
        for k, v in self.payload.items():
            result += f'{k}:{v}\n'
        return result
