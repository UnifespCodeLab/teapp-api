import datetime

from api import db
from sqlalchemy import text


def SerializeCreatedMetadata(entry, user=None):
    if user is None:
        name = db.session.execute(f"SELECT * FROM usuarios WHERE id = {entry.created_user}").first().name
    else:
        name = user.name

    return {
        "created": {
            "user": entry.created_user,
            "name": name,
            "date": entry.created_date.strftime("%Y-%m-%dT%H:%M:%S")
        }
    }


def SerializeUpdatedMetadata(entry, user=None):
    if user is None:
        name = db.session.execute(f"SELECT * FROM usuarios WHERE id = {entry.updated_user}").first().name
    else:
        name = user.name

    return {
        "created": {
            "user": entry.updated_user,
            "name": name,
            "date": entry.updated_date.strftime("%Y-%m-%dT%H:%M:%S")
        }
    }


def SerializeMetadata(entry, into=None, created=None, updated=None):
    # pra só pesquisar uma vez se for o mesmo usuario q criou e atualizou
    user = None
    if entry.created_user == entry.updated_user:
        user = db.session.execute(f"SELECT * FROM usuarios WHERE id = {entry.created_user}").first()

    if into is None:
        into = {}

    serialize_created = created or created is None
    serialize_updated = updated or updated is None

    if serialize_created:
        into = {
            **into,
            **SerializeCreatedMetadata(entry, user),
        }

    if serialize_updated:
        into = {
            **into,
            **SerializeUpdatedMetadata(entry, user),
        }

    return into


def CreateMetadata(entry, user):
    entry.created_date = datetime.datetime.now()
    entry.created_user = user
    entry.updated_date = datetime.datetime.now()
    entry.updated_user = user


def UpdateMetadata(entry, user):
    entry.update({
        "updated_date": datetime.datetime.now(),
        "updated_user": user,
    })
