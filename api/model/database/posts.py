from api import db
import datetime

from api.service.metadata import SerializeMetadata


class Postagem(db.Model):
    __tablename__ = 'postagens'

    id = db.Column(db.Integer, primary_key=True)

    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    titulo = db.Column(db.String(400), nullable=False)
    texto = db.Column(db.String(400), nullable=False)
    selo = db.Column(db.Boolean, default=False, nullable=False)

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
            "categoria": self.categoria,
            "titulo": self.titulo,
            "texto": self.texto,
            "selo": self.selo,
        }

        if metadata or created is not None or updated is not None:
            obj = SerializeMetadata(self, into=obj, created=created, updated=updated)

        return obj
