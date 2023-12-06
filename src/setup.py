from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# Create flask app object 
app = Flask(__name__)

#Set up environment
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
app.json.sort_keys = False


#Initialise
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


