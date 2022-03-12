from sqlalchemy import func

from api import db

from api.model.database.settings import Settings

from api.service.metadata import CreateMetadata, SerializeMetadata
from api.service.privileges import ADMINISTRADOR
from api.service.users import VerifyAccess

from api.util.errors import ForbiddenError, MessagedError


def ByType(type: str):
    active = Settings.query.filter_by(active=True).order_by(Settings.id.desc()).first()
    if active is None:
        active = Settings.query.order_by(Settings.id.desc()).first()

    if active is None:
        raise MessagedError("Não existe uma configuração para esse ambiente. Contate um adminsitrador.")

    data = {}
    if type == 'web':
        data = active.web
    elif type == 'api':
        data = active.api

    visible = data.get("visible", {})

    return {
        "id": active.id,
        "visible": visible
    }

