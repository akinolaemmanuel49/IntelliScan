from datetime import datetime

from intelli_scan.database import db


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
