from flask_cors import cross_origin
from flask_restx import Resource

from api import api
from api.util.auth import get_authorized_user

from api.util.decorators import required

from api.service.privileges import All, Create

import api.model.request.privileges as request
import api.model.response.privileges as response
import api.model.response.default as default

privileges = api.namespace('privileges', description="Privileges namespace")


@privileges.route("")
class Privileges(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=response.privileges_list, token=True)
    def get(self):
        results = All()

        return {"count": len(results), "privileges": results, "success": True}

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.message, request=request.privileges, token=True)
    def post(self, data):
        new_id = Create(data, get_authorized_user())

        return {"message": f"Privilégio {new_id} criado com sucesso"}
