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

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://jkpaprazxcpojo:2a135108dda110cdf26d9ef31fff1c6b9f94cd92993f25a90c3df353c685626d@ec2-52-45-179-101.compute-1.amazonaws.com:5432/d5bi00ifg35edj")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRETKEY', "N5Rc6dvl8giHxExSXQmJ")
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
    cor = db.Column(db.String(10), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    rua = db.Column(db.String(100), nullable=True)
    numero_casa = db.Column(db.Integer, nullable=True)
    data_registro = db.Column(db.DateTime, nullable=True)
    bairro = db.Column(db.Integer, db.ForeignKey('bairros.id'), nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('privilegios.id'), nullable=False)

    def __init__(self, real_name, password, user_name, user_type, bairro):
        import datetime
        self.real_name = real_name
        self.password = password
        self.verificado = False
        self.user_name = user_name
        self.user_type = user_type
        self.data_registro = datetime.datetime.now()
        self.bairro = bairro

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

class Bairro(db.Model):
    __tablename__ = 'bairros'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Postagem(db.Model):
    __tablename__ = 'postagens'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(400), nullable=False)
    texto = db.Column(db.String(400), nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    selo = db.Column(db.Boolean, default=False, nullable=False)
    data = db.Column(db.Time)

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
    postagem = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)
    resposta = db.Column(db.Integer, db.ForeignKey('comentarios.id'), nullable=True)
    data = db.Column(db.Time)

    def __init__(self, texto, criador, postagem, resposta):
        self.texto = texto
        self.criador = criador
        self.postagem = postagem
        self.resposta = resposta

class Form_Socioeconomico(db.Model):
    __tablename__ = 'form_socioeconomico'
    id = db.Column(db.Integer, primary_key=True)
    nome_rep_familia = db.Column(db.String(100), nullable=False)
    pessoa = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    qtd_pessoas_familia = db.Column(db.Integer, nullable=False)
    qtd_criancas = db.Column(db.Integer, nullable=False)
    gestante = db.Column(db.Boolean, nullable=False)
    qtd_amamentando = db.Column(db.Integer, nullable=False)
    qtd_criancas_deficiencia = db.Column(db.Integer, nullable=False)
    preenchido = db.Column(db.Boolean, nullable=False, default="False")
    pessoa_amamenta = db.Column(db.Boolean, nullable=False, default="False")
    qtd_gestantes = db.Column(db.Integer, nullable=False)
    def __init__(self, nome_rep_familia, pessoa, qtd_pessoas_familia, qtd_criancas, gestante, qtd_amamentando, qtd_criancas_deficiencia, qtd_gestantes, pessoa_amamenta):
        self.nome_rep_familia = nome_rep_familia
        self.pessoa = pessoa
        self.qtd_pessoas_familia = qtd_pessoas_familia
        self.qtd_criancas = qtd_criancas
        self.gestante = gestante
        self.qtd_amamentando = qtd_amamentando
        self.qtd_criancas_deficiencia = qtd_criancas_deficiencia
        self.qtd_gestantes = qtd_gestantes
        self.pessoa_amamenta = pessoa_amamenta
        self.preenchido = True

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        try:
            token = request.headers['Authorization'].split("Bearer ")[1]
        except:
            return {'message': 'a valid token is missing'}

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return {'message': 'token is invalid'}
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



@app.route('/form_socio/<id>', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def form_socio(id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_form = Form_Socioeconomico(nome_rep_familia=data['nome_rep_familia'], pessoa=data['pessoa'], qtd_pessoas_familia=data['qtd_pessoas_familia'], 
            pessoa_amamenta=data['pessoa_amamenta'], qtd_criancas=data['qtd_criancas'], gestante=data['gestante'], qtd_amamentando=data['qtd_amamentando'], qtd_criancas_deficiencia=data['qtd_criancas_deficiencia'], qtd_gestantes=data['qtd_gestantes'])
            db.session.add(new_form)
            db.session.commit()

            return {"message": f"Formulário enviado!"}
        else:
            return {"error": "O envio não foi feita no formato esperado"}

    elif request.method == 'GET':
        forms = Form_Socioeconomico.query.all()
        for form in forms:
            if form.preenchido and id == form.pessoa:
                results = [{
                    "respondido": form.preenchido
                }]

        return {"count": len(results), "users": results, "message": "success"}

@app.route('/users', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = Usuario(real_name=data['real_name'], password=data['password'], user_name=data['user_name'], user_type=data['user_type'], bairro=data['bairro'])
            db.session.add(new_user)
            db.session.commit()
            
            new_user = Usuario.query.filter_by(email=data['email'],real_name=data['real_name']).first()
            new_user_not = Notificacoes_Conf(usuario=new_user.id, sistema=False, selo_postagem=False, comentario_postagem=False, saude=False, lazer=False, trocas=False)
            db.session.add(new_user_not)
            db.session.commit()

            return {"message": f"Usuario criado"}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        users = Usuario.query.all()
        results = [
            {
                "user_name": user.user_name,
                "email": user.email
            } for user in users]

        return {"count": len(results), "users": results, "message": "success"}

@app.route('/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = Usuario.query.filter_by(email=data['email']).first()
            if user is None:
                user = Usuario.query.filter_by(user_name=data['user_name']).first()
            if user:
                if user.password == data['password']:
                    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                    token = jwt.encode({'user': toDict(user), 'exp' : expiration}, app.config['SECRET_KEY'], algorithm="HS256")  
                    return {"status": 1000, "type": str(user.user_type), "token": token, "verificado": str(user.verificado)} #Valido
                else:
                    return {"status": 1010} #Invalido
            else:
                return {"status": 1010} #Invalido
        else:
            return {"error": "A requisição não foi feita no formato esperado"}


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

@app.route('/bairros', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def bairros():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_bairro = Bairro(nome=data['nome'])

            db.session.add(new_bairro)
            db.session.commit()

            return {"message": f"Privilégio criado com sucesso"}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        bairros = Bairro.query.all()
        results = [
            {
                "nome": bairro.nome,
                "id": bairro.id
            } for bairro in bairros]

        return {"count": len(results), "Bairros": results, "message": "success"}

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
        categorias = Categoria.query.all()
        results = [
            {
                "nome": categoria.nome,
                "id": categoria.id
            } for categoria in categorias]

        return {"count": len(results), "Categorias": results, "message": "success"}

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
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
        #user.email = data['email']
        #user.real_name = data['real_name']
        #user.password = data['password']
        user.verificado = True
        user.sexo = data['sexo']
        user.nascimento = data['nascimento']
        user.cor = data['cor']
        user.telefone = data['telefone']
        user.rua = data['rua']
        user.numero_casa = data['numero_casa']

        db.session.add(user)
        db.session.commit()

        return {"message": f"Dados de {user.user_name} atualizados"}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {"message": f"Dados de {user.user_name} removidos"}

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
        postagensWithCriador = Postagem.query.join(Usuario, Postagem.criador == Usuario.id, isouter=True).add_columns(Usuario.real_name, Usuario.bairro)

        # filtros gerais
        bairro = request.args.get('bairro', None)
        categoria = request.args.get('categoria', None)

        if categoria is not None:
            postagensWithCriador = postagensWithCriador.filter(Postagem.categoria.in_(map(int, categoria.split(','))))

        if bairro is not None:
            postagensWithCriador = postagensWithCriador.filter(Usuario.bairro.in_(map(int, bairro.split(','))))

        postagens = postagensWithCriador.all()
        results = []
        for post in postagens:
            results.append({"id": post.Postagem.id, "titulo": post.Postagem.titulo,"texto": post.Postagem.texto,"criador": post.real_name,"bairro": post.bairro,"selo":post.Postagem.selo,"categoria":post.Postagem.categoria,"data":post.Postagem.data})

        return {"count": len(results), "post": results, "message": "success"}

@app.route('/recomendados', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def recomendados():
    if request.method == 'GET':
        postagens = Postagem.query.filter_by(selo=True).all()
        results = []
        for post in postagens:
            user = Usuario.query.get_or_404(post.criador)
            results.append({"id": post.id, "titulo": post.titulo,"texto": post.texto,"criador": user.real_name,"selo":post.selo,"categoria":post.categoria})

        return {"count": len(results), "post": results, "message": "success"}

@app.route('/postagens/<id_categoria>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def filtros(id_categoria):
    postagens = Postagem.query.join(Categoria, id_categoria == Postagem.categoria)
    print(postagens)
    results = []
    for post in postagens:
        user = Usuario.query.get_or_404(post.criador)
        results.append({"id": post.id, "titulo": post.titulo,"texto": post.texto,"criador": user.real_name,"selo":post.selo,"categoria":post.categoria, "data": post.data})

    return {"count": len(results), "post": results, "message": "success"}

@app.route('/lista_postagens/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def lista_postagens(id):
    if request.method == 'GET':
        try :
            postagens = Postagem.query.all()
            user = Usuario.query.get_or_404(id)
            results = []
            for post in postagens:
                if post.criador == user.id:
                    results.append({"titulo": post.titulo,"texto": post.texto,"criador": user.real_name})

            return {"count": len(results), "post": results, "message": "success"}
        except:
            return {"error": 404, "message": "Usuário não encontrado"}

@app.route('/comentarios', methods=['POST', 'GET'])
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
        comments = Comentario.query.all()
        results = [
            {
                "texto": comment.texto,
                "criador": comment.criador,
                "postagem": comment.postagem,
                "resposta": comment.resposta,
                "data": comment.data
            } for comment in comments]

        return {"count": len(results), "comments": results, "message": "success"}

@app.route('/comentarios/<postagem_id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def comentarios_postagem(postagem_id):
    if request.method == 'GET':
        comments = Comentario.query.filter_by(postagem=postagem_id).all()
        users_id = [ comment.criador for comment in comments ]
        users = Usuario.query.filter(Usuario.id.in_(users_id)).all()
        results = [
        {
            "texto": comment.texto,
            "criador": 
                { 
                    "id": comment.criador, 
                    "name": next(filter(lambda user: user.id == comment.criador, users)).real_name  
                },
            "resposta": comment.resposta,
            "data": comment.data
        } for comment in comments]
        return {"user": 1,"count": len(results), "comments": results, "message": "success"}


@app.route('/esqueci_senha', methods=['Get', 'Post'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@token_required
def esqueci_senha():
     if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            usuario = data["id"]
            usuario = int(usuario)
            row = Usuario.query.filter_by(id=usuario).one()
          
            #Conecta e inicia o serviço de email
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            res = smtpObj.starttls()

            #Criei essa conta para mandar o email
            smtpObj.login('codelabtesteesquecisenha@gmail.com', '44D6DDAAC9C660F72D6490D7CC44731BEA7C236A9241B387D3E9AF0C66B30D49')
            
            #Gera uma hash que servirá como senha temporaria 
            hash = str(random.getrandbits(128))
            email =  row.email
            row.password = hash
            db.session.add(row)
            db.session.commit()
            msg = "\n\nSua nova senha e " +hash
            smtpObj.sendmail('codelabtesteesquecisenha@gmail.com',email,  msg )
            
            return("A senha temporaria foi enviada para o email " + row.email)
        
        else:
            return {"error": "A requisição não está no formato esperado"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)