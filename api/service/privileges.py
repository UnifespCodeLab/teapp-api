from api import db

from api.model.database.privileges import Privilegio
from api.service.metadata import CreateMetadata
from api.util.errors import BadFormatError, ForbiddenError

ADMINISTRADOR = 1
MODERADOR = 2
USUARIO_COMUM = 3


def All():
    privileges = Privilegio.query.all()
    return [privilege.serialize() for privilege in privileges]


def Create(data, creator):
    new_privilege = Privilegio(name=data['name'])

    CreateMetadata(new_privilege, creator.id)

    db.session.add(new_privilege)
    db.session.commit()

    return new_privilege.id


def Remove(id):
    privilege = Privilegio.query.get_or_404(id)

    if id in [ADMINISTRADOR, MODERADOR, USUARIO_COMUM]:
        raise ForbiddenError(f"Não é possível remover o privilégio padrão \"{privilege.name}\"")

    db.session.delete(privilege)
    db.session.commit()

    return privilege.serialize()

