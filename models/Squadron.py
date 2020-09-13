from services import db
from sqlalchemy import exc


class Squadron(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    commander = db.Column(db.Integer, db.ForeignKey('user.vid'), nullable=True)
