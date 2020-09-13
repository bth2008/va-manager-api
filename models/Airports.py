from services import db
import os
import csv
# from sqlalchemy import exc


class Airports(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    icao = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def feedup(self, app):
        with app.app_context():
            check = self.query.filter_by(icao='UUDD').first()
            if not check:
                with open(os.path.dirname(__file__)+'/../db_seeds/airfields.csv', 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for i in reader:
                        apt = Airports(icao=i[0], name=i[1], lat=i[2], lon=i[3])
                        db.session.add(apt)
                db.session.commit()
