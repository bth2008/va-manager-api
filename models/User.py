from services import db
from sqlalchemy import exc
from datetime import datetime, timedelta
from uuid import uuid4


class User(db.Model):
    vid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    country = db.Column(db.String(3), unique=False, nullable=True)
    division = db.Column(db.String(3), unique=False, nullable=True)
    firstname = db.Column(db.String(100), unique=False, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)
    ratingpilot = db.Column(db.Integer, unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.vid

    def register_user(self):
        if self.vid and self.firstname and self.lastname \
                and self.country and self.division and self.password:
            try:
                db.session.add(self)
                db.session.commit()
            except exc.IntegrityError:
                return {"success": False,
                        "message": "User with same parameters are already exists"}
        else:
            return {"success": False,
                    "message": "Expected vid, firstname, lastname, country, division and password"}
        return {"success": True}

    def generate_auth_token(self):
        if self.vid:
            at = AuthTokens.query.filter(AuthTokens.vid == self.vid,
                                         AuthTokens.token_expires > datetime.now()).first()
            if not at:
                at = AuthTokens(vid=self.vid, token=str(uuid4()), token_expires=datetime.now()+timedelta(hours=1))
                db.session.add(at)
                db.session.commit()
            return at.token
        else:
            return False


class AuthTokens(db.Model):
    vid = db.Column(db.Integer, db.ForeignKey('user.vid'), nullable=False, primary_key=True)
    token = db.Column(db.String(120), unique=True, nullable=False)
    token_expires = db.Column(db.DATETIME, nullable=False)
