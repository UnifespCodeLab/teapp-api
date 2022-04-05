from flask import request as req
from flask_cors import cross_origin
from flask_restx import Resource

from api import api
from api.util.decorators import required, token_required
from api.util.auth import get_authorized_user
from api.util.request import get_boolean_arg, get_string_list_arg
from api.util.errors import MessagedError

from api.service.users import All, VerifyUsername, Create, ById, UpdateById, Remove

import api.model.request.users as request
import api.model.response.users as response
import api.model.response.default as default

users = api.namespace('users', description="Users namespace")


@users.route("")
class User(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=response.users_list, token=True)
    def get(self):
        users = All(not get_boolean_arg("inactive"), get_string_list_arg("email"), get_string_list_arg("username"))

        return {"count": len(users), "users": users, "message": "success"}

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=response.user_create_message, request=request.user_create, token=True)
    def post(self, data):
        try:
            id = Create(data, get_authorized_user())
        except MessagedError as e:
            return {"success": False, "message": e.message}

        return {"success": True, "message": f"Usuario criado", "user": id}


@users.route('/<int:id>')
class UserId(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    # @required(response=response.user_message, token=True)
    @token_required
    def get(self, id):
        user = ById(id, get_boolean_arg("with_data", False))

        return {"success": True, "user": user}

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.message, request=request.user_update, token=True)
    def put(self, data, id):
        try:
            user = UpdateById(id, data, get_authorized_user())

            return {"message": f"Dados de {user['username']} atualizados"}
        except MessagedError as e:
            # erro geral, que possui alguma mensagem especifica
            # nesse caso, informar a mensagem ed erro pro usuario E um status code 500 INTERNAL SERVER ERROR
            return {"message": e.message}

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.message, token=True)
    def delete(self, id):
        try:
            user = Remove(id, get_authorized_user())

            return {"message": f"Dados de {user['username']} removidos"}
        except MessagedError as e:
            # erro geral, que possui alguma mensagem especifica
            # nesse caso, informar a mensagem ed erro pro usuario E um status code 500 INTERNAL SERVER ERROR
            return {"message": e.message}


@users.route("/verify/<string:username>")
class Verify(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.success_message, token=True)
    def get(self, username):
        exists = VerifyUsername(username)

        if exists:
            return {"success": False, "message": f"Usuário '{username}' já existe."}
        else:
            return {"success": True, "message": f"Nome de usuário '{username}' esta disponível."}
