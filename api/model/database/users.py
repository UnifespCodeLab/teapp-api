from api import db

from api.service.metadata import SerializeMetadata


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.Integer, db.ForeignKey('privilegios.id'), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    # ou o usuário tem um email e/ou um nome de usuario
    email = db.Column(db.String(120), unique=True, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(180), nullable=False)
    has_accepted_terms = db.Column(db.Boolean, default=False)

    # dados necessarios pro fork local? não vejo mt a necessidade de criar uma tabela pra isso se as vantagens do
    #      banco relacional não vão ser relevantes
    #      um problema seria a falta de um "schema" pra isso, e talvez a necessidade de salvar um schema também?
    #      esse schema ficaria onde, em uma tabela "config" com coisas do fork?
    #      no exemplo do campo "bairro" pro ibeapp, seria um id dentro de dados ou uma string com o nome do bairro?
    #      se fosse um id, onde ficaria a relação de id_bairro -> nome do bairro? talvez uma tabela geral chamada
    #      "metadados", com colunas como o tipo de dado, id e nome? talvez ficasse "fixa" no código?
    #      se esse campo "bairro" nunca for utilizado como WHERE/JOIN em query, ele não precisa ser "relacional" em
    #      nenhum sentido
    #      formulario socioeconomico estaria dentro disso também?
    #      notificacoes_conf também?
    data = db.Column(db.JSON(), nullable=True)

    # creation/update
    created_date = db.Column(db.DateTime, nullable=False)
    created_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    updated_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # creation/update

    def update(self, data):
        for key in data:
            setattr(self, key, data[key])

    def serialize(self, data=False, created=None, updated=None, metadata=False):
        obj = {
            "id": self.id,
            "type": self.type,
            "active": self.active,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "has_data": self.data is not None,
            "has_accepted_terms": self.has_accepted_terms
        }

        if data:
            obj = {
                **obj,
                "data": self.data
            }

        if metadata or created is not None or updated is not None:
            obj = SerializeMetadata(self, into=obj, created=created, updated=updated)

        return obj
