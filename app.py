from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Interger, String, Float, Text
from os import environ, path
from dotenv import environ, path
from flask_marshmallow import Marshmallow



application = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlife:///' + os.path.join(basedir, 'users.db')


db = SQLAlchemy(application)
ma = Marshmallow(application)


# Endpoints
@application.route('/')
def landing():
    return 'signup or login'


# User
# Sign up
@application.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    email = request.form['email']
    test = User.query.filter_by(email=email).first
    if test:
        return jsonify(message='That email is already in use, please log in'), 409
    else:
        name = request.form['name']
        password = reqest.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message=f'Welcome aboard {name} 👩‍🍳'), 201



# POST /user data: {id:int, name:str, email:str, password:str}
#log in
# POST /user data: {email:str, password:str}

# Recipe
# POST /recipe/<str:name>/...
# GET /recipes
# GET /recipe/<str:name>
# PUT /recipe/<str:name>...
# DEL /recipe/<str:name>

