from api import api
from flask_restx import fields

credentials = api.model("Credentials", {
    "username": fields.String("username", required=True),
    "password": fields.String("password", required=True)
})

recover_password = api.model("Recover Password", {
    "username": fields.String("username", required=False),
    "email": fields.String("email", required=False)
})
