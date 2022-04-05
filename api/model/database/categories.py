from api import db
from api.service.metadata import SerializeMetadata


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False)

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
            "name": self.name,
        }

        if metadata or created is not None or updated is not None:
            obj = SerializeMetadata(self, into=obj, created=created, updated=updated)

        return obj
