from api import db
from api.model.database.comments import Comentario
from api.model.database.users import Usuario
from api.service.metadata import SerializeMetadata, CreateMetadata, SerializeCreatedMetadata
from api.service.privileges import MODERADOR, ADMINISTRADOR
from api.service.users import VerifyAccess
from api.util.auth import get_authorized_user
from api.util.errors import ForbiddenError


def All():
    comments = Comentario.query.order_by(Comentario.created_date.desc()).all()
    users_id = [comment.created_user for comment in comments]

    users = Usuario.query.filter(Usuario.id.in_(users_id)).all()

    return [
        {
            **comment.serialize(),
            **SerializeCreatedMetadata(comment, next(filter(lambda user: user.id == comment.created_user, users)))
        } for comment in comments]


def ByPost(postagem_id):
    comments = Comentario.query.filter_by(postagem=postagem_id).order_by(Comentario.created_date.desc()).all()
    users_id = [comment.created_user for comment in comments]

    users = Usuario.query.filter(Usuario.id.in_(users_id)).all()

    return [{
        **comment.serialize(),
        **SerializeCreatedMetadata(comment, next(filter(lambda user: user.id == comment.created_user, users)))
    } for comment in comments]


def Create(data, creator):
    new_comment = Comentario(texto=data['texto'], resposta=data.get('resposta', None), postagem=data["postagem"])

    CreateMetadata(new_comment, creator.id)

    db.session.add(new_comment)
    db.session.commit()

    return new_comment.id


def Remove(id, remover):
    comentario = Comentario.query.get_or_404(id)

    if remover.id == comentario.created_user or VerifyAccess(remover, [ADMINISTRADOR, MODERADOR]):
        db.session.delete(comentario)
        db.session.commit()

        return comentario.serialize()
    else:
        raise ForbiddenError("O usuário não tem autorização para essa ação")
