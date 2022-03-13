from api import api
from flask_restx import fields

category = api.model("Create Category", {
    "name": fields.String("name", required=True)
})
