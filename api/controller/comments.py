from flask_cors import cross_origin
from flask_restx import Resource

from api import api

from api.util.decorators import required
from api.util.auth import get_authorized_user

from api.service.comments import All, ByPost, Create, Remove

import api.model.request.comments as request
import api.model.response.comments as response
import api.model.response.default as default
from api.util.errors import MessagedError

comments = api.namespace('comments', description="Comments namespace")


@comments.route("/")
class Comments(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.message, request=request.comment, token=True)
    def post(self, data):
        id = Create(data, get_authorized_user())

        return {"message": f"Comentário {id} registrado"}

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=response.comment_list, token=True)
    def get(self):
        results = All()

        return {"count": len(results), "comments": results, "success": True}


@comments.route("/post/<int:id>")
class CommentsPost(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=response.comment_list, token=True)
    def get(self, id):
        results = ByPost(id)

        return {"success": True, "count": len(results), "comments": results}


@comments.route("/<int:id>")
class CommentsId(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    @required(response=default.message, token=True)
    def delete(self, id):
        try:
            Remove(id, get_authorized_user())

            return {"message": f"Comentário {id} removido com sucesso"}
        except MessagedError as e:
            # erro geral, que possui alguma mensagem especifica
            # nesse caso, informar a mensagem ed erro pro usuario E um status code 500 INTERNAL SERVER ERROR
            return {"message": e.message}
