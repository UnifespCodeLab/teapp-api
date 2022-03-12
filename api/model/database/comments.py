import imp
from api import db
import datetime

from api.service.metadata import SerializeMetadata


class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)

    texto = db.Column(db.String(400), nullable=False)
    postagem = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)
    resposta = db.Column(db.Integer, db.ForeignKey('comentarios.id'), nullable=True)

    # creation/update
    created_date = db.Column(db.DateTime, nullable=False)
    created_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    updated_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # creation/update

    def update(self, data):
        for key in data:
            setattr(self, key, data[key])

    def serialize(self, created=None, updated=None, metadata=False):
        obj = {
            "id": self.id,
            "texto": self.texto,
            "postagem": self.postagem,
            "resposta": self.resposta,
        }

        if metadata or created is not None or updated is not None:
            SerializeMetadata(self, into=obj, created=created, updated=updated)

        return obj
