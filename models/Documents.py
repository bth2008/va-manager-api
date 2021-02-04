from services import db
from sqlalchemy import exc


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    body = db.Column(db.TEXT, nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.vid'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add_doc(self, user, data):
        try:
            self.author = user.vid
            self.name = data['name']
            self.lang = data['lang']
            self.body = data['body']
            db.session.add(self)
            db.session.commit()
            return {"success": True}
        except exc.IntegrityError:
            return {"success": False, "message": "Some problem with add document"}

    def del_doc(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"success": True}
        except exc.IntegrityError:
            return {"success": False, "message": "No documents found"}

    def save_doc(self, body):
        try:
            self.body = body['content']
            db.session.commit()
            return {"success": True}
        except exc.IntegrityError:
            return {"success": False, "message": "No documents found"}