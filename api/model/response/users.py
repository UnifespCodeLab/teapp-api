from api import api
from flask_restx import fields

user = api.model("User", {
    "id": fields.Integer,
    "type": fields.Integer,
    "active": fields.Boolean,
    "email": fields.String,
    "username": fields.String,
    "name": fields.String
})

user_data = api.model("User Data", {
    # "sexo": fields.String(max_length=1),
    # "nascimento": fields.String(),
    # "cor": fields.String(),
    # "telefone": fields.String(),
    # "rua": fields.String(),
    # "numero_casa": fields.Integer()
})

user_complete = api.inherit("User Complete", user, {
    "data": fields.Nested(user_data, allow_null=True)
})

user_message = api.model("User Message", {
    "success": fields.Boolean(),
    "user": fields.Nested(user_complete)
})

users_list = api.model("Users List", {
    "count": fields.Integer(),
    "users": fields.List(fields.Nested(user))
})

user_create_message = api.model("User Create Message", {
    "message": fields.String(),
    "user": fields.Integer()
})
