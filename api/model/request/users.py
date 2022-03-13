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
    "type": fields.Integer,
    "active": fields.Boolean,
    "email": fields.String,
    "username": fields.String,
    "name": fields.String,
    "password": fields.String("password"),
    "confirmation_password": fields.String("password"),
    "data": fields.Nested(user_data, skip_none=True)
})

