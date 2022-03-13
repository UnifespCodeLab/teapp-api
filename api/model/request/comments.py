from api import api
from flask_restx import fields

comment = api.model("Comment Create", {
    "postagem": fields.Integer(),
    "texto": fields.String(),
    "resposta": fields.Integer(),
})
