from api import api
from flask_restx import fields

post_create = api.model("Post Create", {
    "categoria": fields.Integer(),
    "titulo": fields.String(),
    "texto": fields.String()
})
