from flask import request
from sqlalchemy import func

from api import db

from api.service.comments import ByPost

from api.model.database.posts import Postagem
from api.model.database.categories import Categoria
from api.model.database.comments import Comentario
from api.model.database.users import Usuario
from api.service.metadata import CreateMetadata, UpdateMetadata, SerializeMetadata
from api.service.privileges import ADMINISTRADOR, MODERADOR
from api.service.users import VerifyAccess
from api.util.errors import ForbiddenError


def All(recommended=None, categories=None, creators=None, bairros=None):
    postagens = Postagem.query.outerjoin(Comentario).add_columns(func.count(Comentario.id).label('comments_count')).group_by(Postagem.id).order_by(Postagem.created_date.desc())

    # filtros gerais
    if recommended is not None:
        postagens = postagens.filter(Postagem.selo == recommended)

    if categories is not None:
        postagens = postagens.filter(Postagem.categoria.in_(categories))

    if creators is not None:
        postagens = postagens.filter(Postagem.created_user.in_(creators))

    # if bairro is not None:
    #     postagens = postagens.filter(Usuario.bairro.in_(bairros))

    postagens = postagens.all()
    results = []
    for post in postagens:
        results.append({
            **post.Postagem.serialize(metadata=True),
            "comments_count": post.comments_count,
        })

    return results


def ById(id):
    post = Postagem.query.filter_by(id=id).first()
    comments = ByPost(post.id)

    result = {
        **post.serialize(metadata=True),
        "comments_count": len(comments),
        "comments": comments
    }

    return result


def Create(data, creator):
    new_post = Postagem(titulo=data['titulo'], texto=data['texto'], categoria=data['categoria'])

    CreateMetadata(new_post, creator.id)

    db.session.add(new_post)
    db.session.commit()

    return new_post.id


def UpdateStamp(id, status, updater):
    postagem = Postagem.query.get_or_404(id)
    postagem.selo = status

    UpdateMetadata(postagem, updater.id)

    db.session.add(postagem)
    db.session.commit()


def Remove(id, remover):
    postagem = Comentario.query.get_or_404(id)

    if remover.id == postagem.created_user or VerifyAccess(remover, [ADMINISTRADOR, MODERADOR]):
        comments = Comentario.query.filter_by(postagem=id).order_by(Comentario.data.desc()).all()
        for comment in comments:
            db.session.delete(comment)

        db.session.delete(postagem)
        db.session.commit()

        return postagem.serialize()
    else:
        raise ForbiddenError("O usuário não tem autorização para essa ação")
