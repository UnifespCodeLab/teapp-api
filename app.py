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
    user_type = db.Column(db.Integer, db.ForeignKey('privilegios.id'), nullable=False)

    def __init__(self, real_name, user_name, verificado, password, email, user_type):
        self.real_name = real_name
        self.password = password
        self.verificado = verificado
        self.email = email
        self.user_type = user_type


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

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(400), nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    postagem = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)
    resposta = db.Column(db.Integer, db.ForeignKey('comentarios.id'), nullable=True)


@app.route('/')
def hello():
	return "Hello World!"

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = Usuario(real_name=data['real_name'], password=data['password'], email=data['email'], user_type=data['user_type'])
            db.session.add(new_user)
            db.session.commit()

            return {"message": f"User {new_user.email} has been created successfully."}
        else:
            return {"error": "The request payload is not in the expected format"}

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
            return {"error": "The request payload is not in the expected format"}


@app.route('/privileges', methods=['POST', 'GET'])
def privileges():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_privilege = Privilegio(user_type=data['user_type'])

            db.session.add(new_privilege)
            db.session.commit()

            return {"message": f"Privilege {new_privilege.user_type} has been created successfully."}
        else:
            return {"error": "The request payload is not in the expected format"}

    elif request.method == 'GET':
        privileges = Privilegio.query.all()
        results = [
            {
                "user_type": privilege.user_type
            } for privilege in privileges]

        return {"count": len(results), "Privileges": results, "message": "success"}

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    user = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "name": user.user_name,
            "model": user.email
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user.email = data['email']
        user.real_name = data['real_name']
        user.password = data['password']
        user.user_type = data['user_type']

        db.session.add(user)
        db.session.commit()

        return {"message": f"User {user.user_name} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {"message": f"User {user.email} successfully deleted."}

@app.route('/postagens', methods=['POST', 'GET'])
def postagens():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_post = Postagem(texto=data['texto'], criador=data['criador'], titulo=data['titulo'])

            db.session.add(new_post)
            db.session.commit()

            return {"message": f"Post {new_post.titulo} has been created successfully."}
        else:
            return {"error": "The request payload is not in the expected format"}

    elif request.method == 'GET':
        postagens = Postagem.query.all()
        results = [
            {
                "titulo": post.titulo,
                "texto": post.texto,
                "criador": post.criador
            } for post in postagens]

        return {"count": len(results), "posts": results, "message": "success"}

@app.route('/comentarios', methods=['POST', 'GET'])
def comentarios():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_comment = Comentario(texto=data['texto'], criador=data['criador'], resposta=data['resposta'], postagem=data["postagem"])

            db.session.add(new_comment)
            db.session.commit()

            return {"message": f"New comment registred."}
        else:
            return {"error": "The request payload is not in the expected format"}

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
