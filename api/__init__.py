import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api

VERSION = "2.0"
AUTH_VERSION = str(os.environ.get("AUTH_VERSION", "0.2.2"))
PORTAL_NAME = "TEApp"

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://sggchwrdaaposg:81d05be684e25e547e89ceb4b30c229926163f02a1091c6d668424296f85f4cd@ec2-54-157-15-228.compute-1.amazonaws.com:5432/dd01iafe525312")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "N5Rc6dvl8giHxExSXQmJ")
app.config['RESTX_MASK_SWAGGER'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app, version=VERSION, title=f"PlaSMeDIS API ({PORTAL_NAME})", description=f"PlaSMeDIS API ({PORTAL_NAME})", doc="/docs")