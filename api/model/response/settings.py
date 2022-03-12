from api import api
from flask_restx import fields


visible = api.schema_model("Visibility", {
    "type": "object"
})

settings = api.model("Settings", {
    "id": fields.Integer(),
    "visible": fields.Nested(visible)
})

settings_response = api.model("Settings Response", {
    "success": fields.Boolean(),
    "message": fields.String(),
    "settings": fields.Nested(settings)
})
