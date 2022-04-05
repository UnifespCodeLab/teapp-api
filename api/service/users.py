from api import db
from api.model.database.users import Usuario

from api.service.metadata import SerializeMetadata, CreateMetadata, UpdateMetadata
from api.service.privileges import ADMINISTRADOR, MODERADOR
from api.util.dict import get_update_dict

from api.util.errors import EntryNotFoundError, BadFormatError, ForbiddenError


# TODO: padronizar respostas dos endpoints?
def All(active_only=True, email=None, username=None):
    query = Usuario.query.order_by("id")

    if active_only:
        query = query.filter_by(active=True)

    if email is not None:
        query = query.filter(Usuario.email.in_(email))

    if username is not None:
        query = query.filter(Usuario.username.in_(username))

    users: list[Usuario] = query.all()

    return [user.serialize(metadata=True) for user in users]


def ById(id, include_data=False):
    user = Usuario.query.get_or_404(id)

    # da pra diminuir o tamanho da resposta só mandando "data" quando for necessário
    #   (já que pode ser relativamente grande dependendo do "fork")
    return user.serialize(data=include_data, metadata=True)


def ByEmail(email):
    return Usuario.query.filter_by(email=email).first()


def ByUsername(username):
    return Usuario.query.filter_by(username=username).first()


def ByUsernameOrEmail(username, email):
    if username is None or username == '':
        user = ByEmail(email)
        if user is None:
            raise EntryNotFoundError(email, f"O email '{email}' não existe")
    else:
        user = ByUsername(username)
        if user is None:
            raise EntryNotFoundError(username, f"O nome de usuário '{username}' não existe")

    return user


def Create(data, creator):
    has_username_or_email = "email" in data or "username" in data

    if not has_username_or_email:
        raise BadFormatError("Usuário deve possuir um email ou nome de usuário")

    new_user = Usuario(type=data.get('type', 3), password=data['password'], name=data['name'])

    if "email" in data:
        new_user.email = data['email']

    if "username" in data:
        new_user.username = data['username']

    CreateMetadata(new_user, creator.id)

    db.session.add(new_user)
    db.session.commit()

    return new_user.id


def UpdateById(id, data, updater):
    is_updated_admin = VerifyAccess(updater, [ADMINISTRADOR])
    is_updated_mod = VerifyAccess(updater, [MODERADOR])
    user = Usuario.query.get_or_404(id)

    if not is_updated_mod and is_updated_admin and updater.id != id:
        raise ForbiddenError("O usuário não tem autorização para essa ação")

    schema = ["name", "has_accepted_terms", "data"]

    # somente um administrador pode alterar as credenciais de usuario
    #   ou o proprio usuario
    if is_updated_admin or updater.id == id:
        # arrumar um jeito melhor pra definir esse tipo de permissao

        schema += ["email", "username"]
        if "password" in data and "confirmation_password" in data and data["password"] == data["confirmation_password"]:
            schema += ["password"]

        # somente um administrador pode mudar o tipo de usuário/desativar
        if is_updated_admin:
            schema += ["type", "active"]

    user_update = get_update_dict(schema, data)
    if user_update is None:
        raise BadFormatError("A requisição não foi feita no formato esperado")

    user.update(user_update)
    UpdateMetadata(user, updater.id)

    db.session.commit()

    return user.serialize()


def UpdatePassword(user, new_password):
    if "password" not in user:
        user = Usuario.query.get_or_404(user.id if "id" in user else user)

    user.password = new_password

    db.session.add(user)
    db.session.commit()

    return user.serialize()


def Remove(id, remover):
    if not VerifyAccess(remover, [ADMINISTRADOR]):
        raise ForbiddenError("O usuário não tem autorização para essa ação")

    user = Usuario.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return user.serialize()


def VerifyUsername(username):
    # entao na hora de "reativar" um usuario tem q checar se alguem pegou o username dele
    return Usuario.query.filter_by(username=username, active=True).first() is not None


def VerifyCredentials(handle, password):
    # filter by username or email
    user = Usuario.query.filter_by(username=handle, active=True).first()  # entao na hora de "reativar" um usuario tem q checar se alguem pegou o username dele
    if user is None:
        user = Usuario.query.filter_by(email=handle, active=True).first()

    if user.password == password:
        return user.serialize()

    return None


def VerifyAccess(user, accepted: list, rejected=None) -> bool:
    if rejected is None:
        rejected = []

    return user.type in accepted and type not in rejected