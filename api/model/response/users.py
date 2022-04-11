from api import api
from flask_restx import fields

user = api.model("User", {
    "id": fields.Integer,
    "type": fields.Integer,
    "active": fields.Boolean,
    "email": fields.String,
    "username": fields.String,
    "name": fields.String,
    "has_data": fields.Boolean,
    "has_accepted_terms": fields.Boolean
})

user_data = api.schema_model("User Data", {
    # 'required': ['address'],
    'properties': {
      'genero': {'type': 'string'},
      'nascimento': {'type': 'date'},
      'area_atuacao': {'type': 'string'},
      'instituicao': {'type': 'string'},
      'campus': {'type': 'string'},
      'setor': {'type': 'string'},
      'deficiencia': {'type': 'boolean'},
      'parente_com_tea': {'type': 'boolean'},
      'freq_convivio_tea': {'type': 'string'},
      'qtd_alunos_tea': {'type': 'integer'},
      'tempo_trabalho_tea': {'type': 'integer'},
      'qtd_pacientes_tea_ano': {'type': 'integer'},
    },
    'type': 'object'
})

user_complete = api.inherit("User Complete", user, {
    "data": fields.Nested(user_data, allow_null=True)
})

user_message = api.model("User Message", {
    "success": fields.Boolean(),
    "user": fields.Nested(user_complete)
})

users_list = api.model("Users List", {
    "count": fields.Integer(),
    "users": fields.List(fields.Nested(user))
})

user_create_message = api.model("User Create Message", {
    "message": fields.String(),
    "user": fields.Integer()
})
