from api import api
from flask_restx import fields

created = api.model("Created Metadata", {
    "user": fields.Integer(),
    "name": fields.String(),
    "date": fields.String()
})

updated = api.model("Updated Metadata", {
    "user": fields.Integer(),
    "name": fields.String(),
    "date": fields.String()
})

metadata = api.model("Metadata", {
    "created": fields.Nested(created),
    "updated": fields.Nested(updated)
})
