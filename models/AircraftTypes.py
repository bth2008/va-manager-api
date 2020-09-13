from services import db
import os
import csv
# from sqlalchemy import exc


class AircraftTypes(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    icao = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    wake_turb = db.Column(db.String(1), nullable=False)
    max_pax = db.Column(db.Integer, nullable=False, default=0)

    def feedup(self, app):
        with app.app_context():
            check = AircraftTypes.query.filter_by(icao='ZULU').first()
            if not check:
                with open(os.path.dirname(__file__)+'/../db_seeds/actypes.csv', 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for i in reader:
                        apt = AircraftTypes(icao=i[0], description=i[1], wake_turb=i[2])
                        db.session.add(apt)
                db.session.commit()
