from api import api
from flask_restx import fields

privileges = api.model("Privileges", {
    "id": fields.Integer,
    "name": fields.String
})

privileges_list = api.model("Privileges List", {
    "count": fields.Integer,
    "privileges": fields.List(fields.Nested(privileges)),
    "success": fields.Boolean
})
