from flask import jsonify, Response, json, request
from models import User


class UserController:
    def __init__(self, config):
        self.controller = 'UserController'
        self.config = config

    def register(self):
        if self.config['app']['ivao_authentication'] == 'true':
            return Response("Direct registration switched off due to ivao authentication", 403)
        user = User(**request.json)
        success = user.register_user()
        if success['success']:
            return jsonify(success)
        else:
            return Response(json.dumps(success), 405,
                            headers={"Content-Type": "application/json"})

    def login(self):
        if self.config['app']['ivao_authentication'] == 'true':
            return Response("Direct authentication switched off due to ivao authentication", 403)
        user = User.query.filter_by(vid=request.json['vid'], password=request.json['password']).first()
        if not user:
            return Response(json.dumps({"success": False, "message": "vid or password is incorrect!"}), 401)
        token = user.generate_auth_token()
        if token:
            return jsonify({"success": True, "token": token})
        else:
            return Response(json.dumps({"success": False, "message": "vid or password is incorrect!"}), 401)
