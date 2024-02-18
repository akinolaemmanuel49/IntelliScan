from intelli_scan.database import db
from intelli_scan.database.models import BaseModel


class InferenceModel(BaseModel):
    """Generates the inferences table"""
    __tablename__ = 'inferences'

    file = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
