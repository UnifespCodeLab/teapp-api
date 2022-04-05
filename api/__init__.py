import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api

AUTH_VERSION = str(os.environ.get("AUTH_VERSION", "0.2.2"))
VERSION = str(os.environ.get("VERSION", "2.1"))
PORTAL_NAME = str(os.environ.get("PORTAL_NAME", "TEApp"))

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "N5Rc6dvl8giHxExSXQmJ")
app.config['RESTX_MASK_SWAGGER'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app, version=VERSION, title=f"PlaSMeDIS API ({PORTAL_NAME})", description=f"PlaSMeDIS API ({PORTAL_NAME})", doc="/docs")
