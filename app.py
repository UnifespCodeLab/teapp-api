from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ykcqisckexhoog:c11398e7afd5548c2dfb0e0f6e7810b1d21cf7dcebc82d58c77577b1a813778e@ec2-50-19-26-235.compute-1.amazonaws.com:5432/d83rhkih4476b9"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verificado = db.Column(db.Boolean, default=False, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    nascimento = db.Column(db.String(20), nullable=False)
    cor = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero_casa = db.Column(db.Integer, nullable=False)
    data_registro = db.Column(db.DateTime, nullable=False)
    bairro = db.Column(db.Integer, db.ForeignKey('bairros.id'), nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('privilegios.id'), nullable=False)

    def __init__(self, real_name, password, email, user_type, sexo, nascimento, cor, telefone, rua, numero_casa):
        import datetime
        self.real_name = real_name
        self.password = password
        self.verificado = False
        self.email = email
        self.user_type = user_type
        self.sexo = sexo
        self.nascimento = nascimento
        self.cor = cor
        self.telefone = telefone
        self.rua = rua
        self.numero_casa = numero_casa
        self.data_registro = datetime.now()

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

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(400), nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    postagem = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)
    resposta = db.Column(db.Integer, db.ForeignKey('comentarios.id'), nullable=True)

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
    def __init__(self, user_type):
        self.user_type = user_type

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = Usuario(real_name=data['real_name'], password=data['password'], email=data['email'], user_type=data['user_type'], bairro=data['bairro'])
            db.session.add(new_user)
            db.session.commit()

            return {"message": f"Usuario criado"}
        else:
            return {"error": "A requisição não foi feita no formato esperado"}

    elif request.method == 'GET':
        users = Usuario.query.all()
        results = [
            {
                "email": user.email
            } for user in users]

        return {"count": len(results), "users": results, "message": "success"}

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = Usuario.query.filter_by(email=data['email']).first()
            if user:
                if user.password == data['password']:
                    return {"status": 1000, "type": str(user.user_type), "id": str(user.id), "verificado": str(user.verificado)} #Valido
                else:
                    return {"status": 1010} #Invalido
            else:
                return {"status": 1010} #Invalido
        else:
            return {"error": "A requisição não foi feita no formato esperado"}


@app.route('/privileges', methods=['POST', 'GET'])
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
                "nome": bairro.nome
            } for bairro in bairros]

        return {"count": len(results), "Bairros": results, "message": "success"}

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    user = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "email": user.email,
            "nome": user.real_name
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        #user.email = data['email']
        #user.real_name = data['real_name']
        user.password = data['password']
        user.verificado = True
        user.sexo = data['sexo']
        user.nascimento = data['nascimento']
        user.cor = data['cor']
        user.telefone = data['telefone']
        user.rua = data['rua']
        user.numero_casa = data['numero_casa']

        db.session.add(user)
        db.session.commit()

        return {"message": f"Dados de {user.email} atualizados"}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {"message": f"Dados de {user.email} removidos"}

@app.route('/postagens', methods=['POST', 'GET'])
def postagens():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_post = Postagem(texto=data['texto'], criador=data['criador'], titulo=data['titulo'])

            db.session.add(new_post)
            db.session.commit()

            return {"message": f"Postagem criada"}
        else:
            return {"error": "A requisição não está no formato esperado"}
    elif request.method == 'GET':
        postagens = Postagem.query.all()
        results = []
        for post in postagens:
            user = Usuario.query.get_or_404(post.criador)
            results.append({"titulo": post.titulo,"texto": post.texto,"criador": user.real_name})

        return {"count": len(results), "post": results, "message": "success"}

@app.route('/lista_postagens/<id>', methods=['GET'])
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
                "resposta": comment.resposta
            } for comment in comments]

        return {"count": len(results), "comments": results, "message": "success"}

if __name__ == '__main__':
    app.run(host="0.0.0.0")
