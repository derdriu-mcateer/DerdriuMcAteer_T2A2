from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError


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

#Error handling

# IntegrityError handler 
@app.errorhandler(IntegrityError)
def handle_integrity_error(err):
    return {"Error": str(err)}, 409

# KeyError handler 
@app.errorhandler(KeyError)
def handle_key_error(err):
    response = f"{err} is required"
    return {"Error": response}, 400

# 400 bad request error handler  
@app.errorhandler(400)
def bad_request(err):
    return {"Error": str(err)}, 400 

# 404 not found error handler
@app.errorhandler(404)
def not_found(err):
    return {"Error": str(err)}, 404 

# 401 unauthorized error handler
@app.errorhandler(401)
def unauthorized(err):
    return {"Error": str(err)}, 401  

# Exception error handler (unexpected errors)
@app.errorhandler(Exception)
def handle_unexpected_error(err):
    return {"Error": str(err)}, 500
