import pathlib
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_apscheduler import APScheduler
from flask_cors import CORS
from configparser import ConfigParser
from services import db, APConfig
from datetime import datetime
from helpers import authenticated
from models import *
from controllers import *

config = ConfigParser()
config.read(pathlib.Path(__file__).parents[0].__str__()+"/config.ini")
version = config['app']['version']
app = Flask(__name__)
app.config.from_object(APConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = config['app']['db_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CORS(app)

def garbage_collection():
    print("Cleaning orphaned token")
    with app.app_context():
        db.init_app(app)
        at = AuthTokens.query.filter(AuthTokens.token_expires <= datetime.now()).all()
        for a in at:
            db.session.delete(a)
        db.session.commit()


@app.route('/')
def main_route():
    return jsonify(f"VA MANAGER API v.{version} by Shakh")


@app.route('/documents')
def all_documents():
    return jsonify(DocController(config).all_docs())


@app.route('/document/<int:doc_id>')
def one_doc(doc_id):
    return jsonify(DocController(config).one_doc(doc_id))

@app.route('/document/save/<int:doc_id>', methods=['POST'])
@authenticated
def save_doc(user, doc_id):
    return jsonify(DocController(config).save_doc(doc_id, user, request.json))

@app.route('/document/add', methods=['POST'])
@authenticated
def add_doc(user):
    return jsonify(DocController(config).add_doc(user, request.json))


@app.route('/document/delete/<int:doc_id>', methods=['DELETE'])
@authenticated
def del_doc(user, doc_id):
    return jsonify(DocController(config).del_doc(user, doc_id))


# When IVAO login api disabled, using this methods
@app.route('/register_user', methods=['POST'])
def register_user():
    """Registering new users"""
    return UserController(config).register()


@app.route('/login_user', methods=['POST'])
def login_user():
    """Returns access token to valid user"""
    return UserController(config).login()

@app.route('/beat')
@authenticated
def beat(user):
    """TODO"""
    return jsonify({"success": True})

if __name__ == "__main__":
    db.init_app(app)
    db.create_all('__all__', app)
    Airports().feedup(app)
    AircraftTypes().feedup(app)
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(config['web']['host'], config['web']['port'])
