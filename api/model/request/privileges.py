from api import api
from flask_restx import fields

privileges = api.model("Privileges", {
    "name": fields.String
})
