from api import api
from flask_restx import fields

comment = api.model("Comment Create", {
    "postagem": fields.Integer("postagem", required=True),
    "texto": fields.String("texto", required=True),
    "resposta": fields.Integer("resposta", required=False),
})
