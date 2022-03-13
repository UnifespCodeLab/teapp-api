from api.util.decorators import required
from api import api
from flask_restx import fields

from api.model.response.users import user, user_complete


login_response = api.model("Login Response", {
    "status": fields.Integer,
    "user": fields.Nested(user, allow_null=True),
    "token": fields.String()
})

auth_version = api.model("Authentication Version", {
    "version": fields.String
})

me = api.inherit("Authorized User", user_complete, {})
