import os
import jwt
from flask import request
from api import app, api
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        try:
            token = request.headers['Authorization'].split("Bearer ")[1]
        except:
            return {'message': 'a valid token is missing'}

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              issuer=os.environ.get('ME', 'plasmedis-api-local'),
                              algorithms=["HS256"],
                              options={
                                  "require": ["exp", "sub", "iss", "aud"],
                                  "verify_aud": False,
                                  "verify_iat": False, "verify_nbf": False
                              })

        except jwt.exceptions.InvalidKeyError:
            return {'message': 'Secret Key is not in the proper format'}
        except jwt.exceptions.InvalidAlgorithmError:
            return {'message': 'Algorithm is not recognized by PyJWT'}
        except jwt.exceptions.ExpiredSignatureError:
            return {'message': 'Token is expired'}
        except jwt.exceptions.InvalidIssuerError:
            return {'message': 'Token has a different issuer'}
        except jwt.exceptions.MissingRequiredClaimError:
            return {'message': 'Token is missing a required claim'}
        except jwt.exceptions.DecodeError:
            return {'message': 'Token failed validation'}
        except Exception as ex:
            return {'message': 'There was a error decoding the token'}

        return f(*args, **kwargs)

    return decorator


def json_required(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        if not request.is_json:
            return {'message': 'Espected json'}, 400
        return f(self, request.get_json(), *args, **kwargs)
    return decorator


def required(response, request=None, token=False):
    def required_decorator(f):
        parser = api.parser()
        if token:
            parser.add_argument("Authorization", location="headers")

        @wraps(f)
        @api.expect(request, parser)
        @api.marshal_with(response)
        def decorator(*args, **kwargs):
            return f(*args, **kwargs)
        
        if token:
            decorator = token_required(decorator)
        if request:
            decorator = json_required(decorator)
        return decorator
        
    return required_decorator

