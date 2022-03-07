from email.policy import default
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import smtplib
import random
import jwt
import datetime
from functools import wraps
from sqlalchemy import func, sql, event
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import relationship


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://jkpaprazxcpojo:2a135108dda110cdf26d9ef31fff1c6b9f94cd92993f25a90c3df353c685626d@ec2-52-45-179-101.compute-1.amazonaws.com:5432/d5bi00ifg35edj")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "N5Rc6dvl8giHxExSXQmJ")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(80), nullable=False)
    user_name = db.Column(db.String(80), unique=True, nullable=False) 
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    verificado = db.Column(db.Boolean, default=False, nullable=False)
    sexo = db.Column(db.String(1), nullable=True)
    nascimento = db.Column(db.String(20), nullable=True)
    data_registro = db.Column(db.DateTime, nullable=True)
    user_type = db.Column(db.Integer, db.ForeignKey('privilegios.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, real_name, password, user_name, user_type):
        self.real_name = real_name
        self.password = password
        self.user_name = user_name
        self.user_type = user_type
        self.data_registro = datetime.datetime.now()

@event.listens_for(Usuario, 'after_insert')
def receive_after_insert(mapper, connection, target):
    new_comp = Complemento_de_Dados(target.id)
    db.session.add(new_comp)

class Complemento_de_Dados(db.Model):
    __tablename__ = 'complemento_de_dados'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete="cascade"), primary_key=True)
    universidade = db.Column(db.String(80), nullable=True)
    campus = db.Column(db.String(80), nullable=True)
    setor = db.Column(db.String(80), nullable=True)
    deficiencia = db.Column(db.String(80), nullable=True)
    parente_com_tea = db.Column(db.String(80), nullable=True)
    freq_convivio_tea = db.Column(db.String(80), nullable=True)
    qtd_alunos_tea = db.Column(db.Integer, nullable=True)
    tempo_trabalho_tea = db.Column(db.Integer, nullable=True)
    qtd_pacientes_tea_ano = db.Column(db.Integer, nullable=True)

    def __init__(self, id):
        self.id = id

class Notificacoes_Conf(db.Model):
    __tablename__ = 'notificacoes_conf'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    sistema = db.Column(db.Boolean, default=False, nullable=False)
    selo_postagem = db.Column(db.Boolean, default=False, nullable=False)
    comentario_postagem = db.Column(db.Boolean, default=False, nullable=False)
    saude =db.Column(db.Boolean, default=False, nullable=False)
    lazer = db.Column(db.Boolean, default=False, nullable=False)
    trocas = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, usuario, sistema, selo_postagem, comentario_postagem, saude, lazer, trocas):
        self.usuario = usuario
        self.sistema = sistema
        self.selo_postagem = selo_postagem
        self.comentario_postagem = comentario_postagem
        self.saude = saude
        self.lazer = lazer
        self.trocas = trocas

class Privilegio(db.Model):
    __tablename__ = 'privilegios'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, user_type):
        self.user_type = user_type

class Postagem(db.Model):
    __tablename__ = 'postagens'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(400), nullable=False)
    texto = db.Column(db.String(400), nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    selo = db.Column(db.Boolean, default=False, nullable=False)
    data = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __init__(self, titulo, texto, criador, categoria):
        self.titulo = titulo
        self.texto = texto
        self.criador = criador
        self.categoria = categoria

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(400), nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    postagem = db.Column(db.Integer, db.ForeignKey('postagens.id', ondelete="cascade"), nullable=False)
    resposta = db.Column(db.Integer, db.ForeignKey('comentarios.id'), nullable=True)
    data = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __init__(self, texto, criador, postagem, resposta):
        self.texto = texto
        self.criador = criador
        self.postagem = postagem
        self.resposta = resposta

def get_authorized_user(request):
    token = request.headers['Authorization'].split("Bearer ")[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], issuer=os.environ.get('ME', 'plasmedis-api-local'),
                      algorithms=["HS256"],
                      options={"require": ["exp", "sub", "iss", "aud"], "verify_aud": False, "verify_iat": False,
                               "verify_nbf": False})
    return payload['sub']

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        try:
            token = request.headers['Authorization'].split("Bearer ")[1]
        except:
            return {'message': 'a valid token is missing'}

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], issuer=os.environ.get('ME', 'plasmedis-api-local'), algorithms=["HS256"], options={"require": ["exp", "sub", "iss", "aud"], "verify_aud": False, "verify_iat": False, "verify_nbf": False})
        except jwt.exceptions.InvalidKeyError:
            return {'message': 'Secret Key is not in the proper format'}
        except jwt.exceptions.InvalidAlgorithmError:
            return {'message': 'Algorithm is not recognized by PyJWT'}
        except jwt.exceptions.ExpiredSignatureError:
            return {'message': 'Token is expired'}
        except jwt.exceptions.InvalidIssuerError:
            return {'message': 'Token has a different issuer'}
        except jwt.exceptions.MissingRequiredClaimError:
            return {'message': 'Token is missing a required claim'}
        except jwt.exceptions.DecodeError:
            return {'message': 'Token failed validation'}
        except Exception as ex:
            return {'message': 'There was a error decoding the token'}

        return f(*args, **kwargs)
   return decorator

def toDict(user: Usuario):
    return {
        "id": user.id,
        "real_name": user.real_name,
        "verificado": user.verificado,
        "user_name": user.user_name,
        "user_type": user.user_type,
        "email": user.email
    }

@app.route('/')
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def hello():
	return "This API Works! [" + os.environ.get("ENV", "DEV") + "]"

@app.route('/me', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def me():
    id = get_authorized_user(request)

    user = Usuario.query.get(id)

    return toDict(user)

@app.route('/users/<id>/notificacoes_conf', methods=['PUT', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def handle_user_notificacao(id):
    user_not = Notificacoes_Conf.query.filter_by(usuario=id).first()

    if request.method == 'GET':
        response = {
            "sistema":user_not.sistema,
            "selo_postagem":user_not.selo_postagem,
            "comentario_postagem":user_not.comentario_postagem,
            "saude":user_not.saude,
            "lazer":user_not.lazer,
            "trocas":user_not.trocas
        }
        return {"message": "success", "user_not": response}
    elif request.method == 'PUT':
        data = request.get_json()
        user_not.sistema = data['sistema']
        user_not.selo_postagem = data['selo_postagem']
        user_not.comentario_postagem = data['comentario_postagem']
        user_not.saude = data['saude']
        user_not.lazer = data['lazer']
        user_not.trocas = data['trocas']
        db.session.add(user_not)
        db.session.commit()
        return {"message": f"Configurações de notificação atualizadas"}

@app.route('/users', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = Usuario(real_name=data['real_name'], password=data['password'], user_name=data['user_name'], user_type=data['user_type'])
            if "email" in data:
                new_user.email = data['email']
            db.session.add(new_user)
            db.session.commit()
            
            new_user = Usuario.query.filter_by(user_name=data['user_name'],real_name=data['real_name']).first()
            new_user_not = Notificacoes_Conf(usuario=new_user.id, sistema=False, selo_postagem=False, comentario_postagem=False, saude=False, lazer=False, trocas=False)
            db.session.add(new_user_not)
            db.session.commit()

            return {"message": f"Usuario criado", "user": new_user.id}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        users = Usuario.query.order_by("id").all()
        results = [
            {
                "id": user.id,
                "user_name": user.user_name,
                "nascimento": user.nascimento,
                "email": user.email,
                "privilegio": user.user_type,
                "is_active": user.is_active
            } for user in users]

        return {"count": len(results), "users": results, "message": "success"}

@app.route('/login', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    AUTH_VERSION = os.environ.get("AUTH_VERSION", 0.2)

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = Usuario.query.filter_by(user_name=data['username'], is_active=True).first()
            if user is None:
                user = Usuario.query.filter_by(email=data['username'], is_active=True).first()
            if user:
                if user.password == data['password']:
                    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                    issuedAt = datetime.datetime.utcnow()
                    token = jwt.encode({'auth': AUTH_VERSION, 'exp': expiration, 'iat': issuedAt, 'sub': user.id, 'iss': os.environ.get('ME', 'plasmedis-api-local'), 'aud': request.args.get('aud', 'unknown')}, app.config['SECRET_KEY'], algorithm="HS256")
                    return {"status": 1000, "user": toDict(user), "token": token, "verificado": str(user.verificado)} #Valido
                else:
                    return {"status": 1010} #Invalido
            else:
                return {"status": 1010} #Invalido
        else:
            return {"error": "A requisição não foi feita no formato esperado"}
    elif request.method == 'GET':
        # retorna um marcador de versão, para quando as mudanças no token forem tão significativas que o único
        # jeito de atualizar algo no front vai ser matando a sessão atual do usuário
        return {'version': AUTH_VERSION}



@app.route('/privileges', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def privileges():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_privilege = Privilegio(user_type=data['user_type'])

            db.session.add(new_privilege)
            db.session.commit()

            return {"message": f"Privilégio criado com sucesso"}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        privileges = Privilegio.query.all()
        results = [
            {
                "user_type": privilege.user_type
            } for privilege in privileges]

        return {"count": len(results), "Privileges": results, "message": "success"}

@app.route('/categorias', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def categorias():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_categoria = Categoria(nome=data['nome'])

            db.session.add(new_categoria)
            db.session.commit()

            return {"message": f"Categoria criado com sucesso"}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        categorias = Categoria.query.outerjoin(Postagem).add_columns(func.count(Postagem.id).label('postagens')).group_by(Categoria.id).all()

        results = [
            {
                "nome": categoria.Categoria.nome,
                "id": categoria.Categoria.id,
                "postagens": categoria.postagens
            } for categoria in categorias]

        return {"count": len(results), "Categorias": results, "message": "success"}

@app.route('/users/<id>', methods=['GET', 'PUT'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def handle_user(id):
    user = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "email": user.email,
            "privilegio": user.user_type,
            "nome": user.real_name,
            "sexo": user.sexo,
            "nascimento": user.nascimento,
            "cor": user.cor,
            "telefone": user.telefone,
            "rua": user.rua,
            "numero_casa": user.numero_casa
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user_data = Complemento_de_Dados.query.get_or_404(id)
        #user.email = data['email']
        #user.real_name = data['real_name']
        #user.password = data['password']
        user.verificado = True
        user.sexo = data['sexo']
        user.nascimento = data['nascimento']
        user_data.universidade = data['universidade']
        user_data.campus = data['campus']
        user_data.setor = data['setor']
        user_data.deficiencia = data['deficiencia']
        user_data.parente_com_tea = data['parente_com_tea']
        user_data.freq_convivio_tea = data['freq_convivio_tea']
        user_data.qtd_alunos_tea = data['qtd_alunos_tea']
        user_data.tempo_trabalho_tea = data['tempo_trabalho_tea']
        user_data.qtd_pacientes_tea_ano = data['qtd_pacientes_tea_ano']

        db.session.add(user_data)
        db.session.add(user)
        db.session.commit()

        return {"message": f"Dados de {user.user_name} atualizados"}


@app.route('/inactivate_users/<id>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def inactivate_user(id):
    user = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        if request.is_json:
            user.is_active = False

            db.session.add(user)
            db.session.commit()
        return {"message": "success"}

@app.route('/activate_users/<id>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def activate_user(id):
    user = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        if request.is_json:
            user.is_active = True

            db.session.add(user)
            db.session.commit()
        return {"message": "success"}

@app.route('/selo/<id>', methods=['PUT'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def selo(id):
    postagem = Postagem.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.get_json()
        postagem.selo = True

        db.session.add(postagem)
        db.session.commit()

        return {"message": f"Selo emitido!"}

@app.route('/postagens', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def postagens():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_post = Postagem(texto=data['texto'], criador=data['criador'], titulo=data['titulo'], categoria=data['categoria'])

            db.session.add(new_post)
            db.session.commit()

            return {"message": f"Postagem criada"}
        else:
            return {"error": "A requisição não está no formato esperado"}
    elif request.method == 'GET':
        postagens = Postagem.query.outerjoin(Comentario).add_columns(func.count(Comentario.id).label('comentarios')).group_by(Postagem.id).order_by(Postagem.data.desc())

        # postagensWithCriador = Postagem.query.join(Usuario, Postagem.criador == Usuario.id, isouter=True).outerjoin(
        #     Comentario).add_columns(Usuario.id, Usuario.real_name, Usuario.bairro, func.count(Comentario.id).label('comentarios')).group_by(Postagem.id, Usuario.id)

        # filtros gerais
        #bairro = request.args.get('bairro', None)
        categoria = request.args.get('categoria', None)

        if categoria is not None:
            postagensWithCriador = postagens.filter(Postagem.categoria.in_(map(int, categoria.split(',')))).order_by(Postagem.data.desc())

        # if bairro is not None:
        #     postagensWithCriador = postagens.filter(Usuario.bairro.in_(map(int, bairro.split(','))))

        postagens = postagens.all()
        results = []
        for post in postagens:
            user = Usuario.query.get_or_404(post.Postagem.criador)
            results.append({"id": post.Postagem.id, "titulo": post.Postagem.titulo, "texto": post.Postagem.texto,
                            "criador": user.real_name, "id_criador": user.id,
                            "selo": post.Postagem.selo,
                            "categoria": post.Postagem.categoria,
                            "data": post.Postagem.data.strftime("%Y-%m-%dT%H:%M:%S"),
                            "comentarios": post.comentarios})

        return {"count": len(results), "post": results, "message": "success"}

@app.route('/recomendados', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def recomendados():
    if request.method == 'GET':
        postagens = db.session.query(Postagem, func.count(Comentario.id).label('comentarios')).outerjoin(Comentario).filter(Postagem.selo == True).group_by(Postagem.id).order_by(Postagem.data.desc())

        results = []
        for post, comentarios in postagens:
            user = Usuario.query.get_or_404(post.criador)
            results.append({"id": post.id, "titulo": post.titulo, "texto": post.texto, "criador": user.real_name,
                            "selo": post.selo, "categoria": post.categoria, "comentarios": comentarios})

        return {"count": len(results), "post": results, "message": "success"}

@app.route('/postagens/categorias/<id_categoria>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def filtros(id_categoria):
    postagens = db.session.query(Postagem, func.count(Comentario.id).label('comentarios')).outerjoin(Comentario).filter(Postagem.categoria == id_categoria).group_by(Postagem.id).order_by(Postagem.data.desc())

    results = []
    for post, comentarios in postagens:
        user = Usuario.query.get_or_404(post.criador)
        results.append(
            {"id": post.id, "titulo": post.titulo, "texto": post.texto, "criador": user.real_name, "id_criador": user.id, "selo": post.selo,
             "categoria": post.categoria, "data": post.data.strftime("%Y-%m-%dT%H:%M:%S"), "comentarios": comentarios})

    return {"count": len(results), "post": results, "message": "success"}

@app.route('/postagens/<id>', methods=['GET','DELETE'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def postagensId(id):
    if request.method == 'GET':
        post = Postagem.query.filter_by(id=id).first()
        #TODO: Criar uma estrutura com 'services' com funções para facilitar a vida (e evitar ter que fazer encode decode do json)
        import json
        comments = comentarios_postagem(post.id).response[0].decode('utf-8')
        comments = json.loads(comments)
        post_user = Usuario.query.get_or_404(post.criador)
        result = {
            "id": post.id,
            "titulo": post.titulo,
            "texto": post.texto,
            "criador": {
                "id": post_user.id,
                "name": post_user.real_name
            },
            "selo":post.selo,
            "categoria":post.categoria,
            "data": post.data.strftime("%Y-%m-%dT%H:%M:%S"),
            "comentarios": comments['comments']
        }
        return result
    elif request.method == 'DELETE':
        post = Postagem.query.filter_by(id=id).first()
        comments = Comentario.query.filter_by(postagem=id).order_by(Comentario.data.desc()).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Postagem removida com sucesso"}

@app.route('/lista_postagens/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def lista_postagens(id):
    if request.method == 'GET':
        try :
            postagens = Postagem.query.order_by(Postagem.data.desc()).all()
            user = Usuario.query.get_or_404(id)
            results = []
            for post in postagens:
                if post.criador == user.id:
                    results.append({"titulo": post.titulo,"texto": post.texto,"criador": user.real_name})

            return {"count": len(results), "post": results, "message": "success"}
        except:
            return {"error": 404, "message": "Usuário não encontrado"}

@app.route('/comentarios', methods=['POST', 'GET', 'DELETE'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def comentarios():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_comment = Comentario(texto=data['texto'], criador=data['criador'], resposta=data['resposta'], postagem=data["postagem"])

            db.session.add(new_comment)
            db.session.commit()

            return {"message": f"Comentário registrado"}
        else:
            return {"error": "A requisição não está no formato esperado"}

    elif request.method == 'GET':
        comments = Comentario.query.order_by(Comentario.data.desc()).all()
        results = [
            {
                "texto": comment.texto,
                "criador": comment.criador,
                "postagem": comment.postagem,
                "resposta": comment.resposta,
                "data": comment.data.strftime("%Y-%m-%dT%H:%M:%S")
            } for comment in comments]

        return {"count": len(results), "comments": results, "message": "success"}

    elif request.method == 'DELETE':
        if request.is_json:
            data = request.get_json()
            comentario = Comentario.query.filter_by(id=data['comentario_id']).first()
            id = get_authorized_user(request)
            usuario = Usuario.query.get(id)
            privilegio_adm = Privilegio.query.filter_by(user_type='Admin').first()
            privilegio_mod = Privilegio.query.filter_by(user_type='Moderador').first()

            if not usuario or not comentario:
                return {"error": "Informações de usuário ou comentário inválidas"}

            if usuario.id == comentario.criador or usuario.user_type == privilegio_adm.id or usuario.user_type == privilegio_mod.id:
                db.session.delete(comentario)
                db.session.commit()
                return {"message": "Comentário removido com sucesso"}

            return {"error": "O usuário não tem autorização para essa ação"}
        
        else:
            return {"error": "A requisição não está no formato esperado"}


@app.route('/comentarios/<postagem_id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def comentarios_postagem(postagem_id):
    if request.method == 'GET':
        comments = Comentario.query.filter_by(postagem=postagem_id).order_by(Comentario.data.desc()).all()
        users_id = [ comment.criador for comment in comments ]
        users = Usuario.query.filter(Usuario.id.in_(users_id)).all()
        results = [
        {
            "id": comment.id,
            "texto": comment.texto,
            "criador":
                {
                    "id": comment.criador,
                    "name": next(filter(lambda user: user.id == comment.criador, users)).real_name
                },
            "resposta": comment.resposta,
            "data": comment.data.strftime("%Y-%m-%dT%H:%M:%S")
        } for comment in comments]
        return {"user": 1,"count": len(results), "comments": results, "message": "success"}


@app.route('/esqueci_senha', methods=['Get', 'Post'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def esqueci_senha():
     if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get("username", None)
            email = data.get("email", None)

            if username is None or username == '':
                row = Usuario.query.filter_by(email=email).first()
                if row is None:
                    return f"O email \"{email}\" não existe"
            else:
                row = Usuario.query.filter_by(user_name=username).first()
                if row is None:
                    return f"O nome de usuário \"{username}\" não existe"


            #Conecta e inicia o serviço de email
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            res = smtpObj.starttls()

            #Criei essa conta para mandar o email
            # https://stackoverflow.com/questions/54657006/smtpauthenticationerror-5-7-14-please-log-n5-7-14-in-via-your-web-browser/56809076#56809076
            smtpObj.login('codelabtesteesquecisenha@gmail.com', '44D6DDAAC9C660F72D6490D7CC44731BEA7C236A9241B387D3E9AF0C66B30D49')

            #Gera uma hash que servirá como senha temporaria
            hash = str(random.getrandbits(128))[:11]
            email =  row.email
            row.password = hash
            db.session.add(row)
            db.session.commit()
           
            msg = MIMEMultipart()
            msg['Subject'] = 'Recuperação de senha Ibeac'
            msg['From'] = 'Ibeac-Senha'
            msg['To'] = email
            body = MIMEText("A sua nova senha é "+hash)
            msg.attach(body) 
            smtpObj.sendmail('codelabtesteesquecisenha@gmail.com',email,  msg.as_string())


            return("A senha temporária foi enviada para o email: " + row.email)

        else:
            return {"error": "A requisição não está no formato esperado"}

@app.route('/users/username/verify/<username>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def verify_username(username):
    user = Usuario.query.filter_by(user_name=username).first()
    if user:
        return { "success": False, "message": "User with username '" + str(username) + "' already exists." }
    else:
        return { "success": True, "message": "Username '" + str(username) + "' is available."}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
