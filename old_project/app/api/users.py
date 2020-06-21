from datetime import datetime

from flask import make_response, jsonify, request, current_app
from flask.views import MethodView

from . import api
from .. import db
from ..models import User

@api.route("/test", methods=["GET"])
def test():
    return "Project setup successfully!", 200

class UserAPI(MethodView):
    def __init__(self):
        self.logger = current_app.logger

    def post(self):
        try:
            json_dict = request.get_json()
        except Exception as e:
            return make_response(jsonify({"error": ["Missing required data"]}), 400)

        first_name = json_dict.get("first_name", None)
        last_name = json_dict.get("last_name", None)
        msisdn = json_dict.get("msisdn", None)

        if not first_name:
            return make_response(jsonify({"error": ["First name is required."]}), 400)
        if not last_name:
            return make_response(jsonify({"error": ["Last name is required."]}), 400)
        if not msisdn:
            return make_response(jsonify({"error": ["Phone number is required."]}), 400)
        if not msisdn.isdigit():
            return make_response(jsonify({"error": ["Phone number must contain just numbers."]}), 400)

        user = User.query.filter(User.msisdn == json_dict["msisdn"]).first()
        if user is not None:
            return make_response(jsonify({"error": ["User with that phone number already exists."]}), 400)

        user = User(created=datetime.utcnow(), msisdn=msisdn, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({"success": "OK", "user": user.to_json()}), 201)


user_post_view = UserAPI.as_view("users_post")

api.add_url_rule("/users/", view_func=user_post_view, methods=["POST"])
