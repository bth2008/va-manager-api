from services import db
# from sqlalchemy import exc


class Fleet(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    acf_type = db.Column(db.Integer, db.ForeignKey('aircraft_types.id'), nullable=False)
    reg_number = db.Column(db.String(10), nullable=False)
    state = db.Column(db.Integer, default=0) #0 - free, 1 - blocked, 2 - enroute
    user_id = db.Column(db.Integer, db.ForeignKey('user.vid'))
    squadron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    location = db.Column(db.Integer, db.ForeignKey('airports.id'))
