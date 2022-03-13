from api import api
from flask_restx import fields

category = api.model("Category", {
    "id": fields.Integer(),
    "name": fields.String("name"),
    "posts": fields.Integer()
})

category_list = api.model("Category List", {
    "success": fields.Boolean(),
    "count": fields.Integer(),
    "categories": fields.List(fields.Nested(category))
})
