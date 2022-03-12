import jwt
import os

from flask import request

from api import app

from api.model.database import users, privileges


def get_authorized_user():
    token = request.headers['Authorization'].split("Bearer ")[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], issuer=os.environ.get('ME', 'plasmedis-api-local'),
                      algorithms=["HS256"],
                      options={"require": ["exp", "sub", "iss", "aud"], "verify_aud": False, "verify_iat": False,
                               "verify_nbf": False})
    id = payload['sub']

    return users.Usuario.query.get(id)
