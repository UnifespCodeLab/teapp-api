from flask import request as req
from flask_cors import cross_origin
from flask_restx import Resource

from api import api, AUTH_VERSION

from api.util.decorators import required, token_required
from api.util.auth import get_authorized_user
from api.util.errors import EntryNotFoundError, MessagedError, NotFoundError
from api.util.request import get_boolean_arg

from api.service.settings import *

import api.model.response.settings as response
import api.model.response.default as default

settings = api.namespace('settings', description="Settings namespace")


@settings.route("/<string:type>")
class Settings(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @token_required
    def get(self, type):
        if type not in ['web', 'api']:
            return {"success": False, "message": f"Não existe uma configuração para \"{type}\""}

        data = ByType(type)

        return {"success": True, "message": "Recuperando configuração atual", "settings": data}
