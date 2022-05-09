from api import api
from flask_restx import fields

user_data = api.model("User Data", {
    # "sexo": fields.String(max_length=1),
    # "nascimento": fields.String(),
    # "cor": fields.String(),
    # "telefone": fields.String(),
    # "rua": fields.String(),
    # "numero_casa": fields.Integer()
})

user_create = api.model("User Create", {
    "type": fields.Integer(3),
    "username": fields.String("username"),
    "email": fields.String("user@user.com"),
    "name": fields.String("name"),
    "password": fields.String("password"),
    "data": fields.Nested(user_data, allow_null=True)
})

user_update = api.model("User Update", {
    "type": fields.Integer("type", required=False),
    "active": fields.Boolean("active", required=False),
    "email": fields.String,
    "username": fields.String,
    "name": fields.String,
    "current_password": fields.String("current_password", required=False),
    "password": fields.String("password", required=False),
    "confirmation_password": fields.String("confirmation_password", required=False),
    "data": fields.Nested(user_data, skip_none=True)
})

