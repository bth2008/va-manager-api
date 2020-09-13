import requests
import json
from functools import wraps
from flask import request, Response
from configparser import ConfigParser
from models import User, AuthTokens
from services import db
from datetime import datetime, timedelta

config = ConfigParser()
config.read("config.ini")


def bearer_autheticator(req):
    try:
        token = req.headers.get("Authorization").split("Bearer ")[1]
        userdata = AuthTokens.query.filter(AuthTokens.token == token,
                                           AuthTokens.token_expires > datetime.now()).first()
        if not userdata and config['app']['ivao_authentication'] != 'true':
            return False
        # this block works only when ivao_authenticaton switched on
        if not userdata:  # token not found or expires
            userdata = requests.get(f"{config['app']['ivao_login_url']}?token={token}&type=json").json()
            if not userdata['result']:
                return False
            user = User.query.filter_by(vid=userdata['vid']).first()
            if not user:  # user not found. so let's create one
                user = User(vid=userdata['vid'], country=userdata['country'], division=userdata['division'],
                            firstname=userdata['firstname'], lastname=userdata['lastname'],
                            ratingpilot=userdata['ratingpilot'])
                authtoken = AuthTokens(vid=userdata['vid'], token=token,
                                       token_expires=datetime.now()+timedelta(hours=1))
                db.session.add(user)
                db.session.add(authtoken)
                db.session.commit()
        else:
            userdata.token_expires = datetime.now() + timedelta(hours=1)
            db.session.commit()
            user = User.query.filter_by(vid=userdata.vid).first()
        return user
    except (AttributeError, IndexError):
        return False


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = bearer_autheticator(request)
        if user:
            kwargs['user'] = user
            return func(*args, **kwargs)
        else:
            return Response(json.dumps({"success": False, "message": "Forbidden access"}), 403,
                            headers={"Content-Type": "application/json"})
    return wrapper
