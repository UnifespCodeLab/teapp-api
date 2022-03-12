from sqlalchemy import func

from api import db

from api.model.database.categories import Categoria
from api.model.database.posts import Postagem

from api.service.metadata import CreateMetadata, SerializeMetadata
from api.service.privileges import ADMINISTRADOR
from api.service.users import VerifyAccess
from api.util.errors import ForbiddenError


def All():
    categorias = Categoria.query.outerjoin(Postagem).add_columns(func.count(Postagem.id).label('postagens')).group_by(Categoria.id).order_by(Categoria.id).all()

    return [
        {
            **categoria.Categoria.serialize(),
            "posts": categoria.postagens
        } for categoria in categorias]


def ById(id):
    categoria = Categoria.query.get_or_404(id)
    posts = Postagem.query.filter_by(categoria=id).all()

    return {
        **categoria.Categoria.serialize(metadata=True),
        "posts": len(posts),
    }


def Create(data, creator):
    new_categoria = Categoria(name=data['name'])

    CreateMetadata(new_categoria, creator.id)

    db.session.add(new_categoria)
    db.session.commit()

    return new_categoria.id


def Remove(id, replacement, remover):
    if not VerifyAccess(remover, [ADMINISTRADOR]):
        raise ForbiddenError("O usuário não tem autorização para essa ação")

    if id == 0:
        raise ForbiddenError(f"Não é possivel remover essa categoria")

    categoria = Categoria.query.get_or_404(id)

    if replacement is not None:
        Postagem.query.filter(Postagem.categoria == id).update({"categoria": replacement})
    else:
        Postagem.query.filter(Postagem.categoria == id).update({"categoria": 0})

    db.session.delete(categoria)
    db.session.commit()

    return categoria.serialize(metadata=True)
