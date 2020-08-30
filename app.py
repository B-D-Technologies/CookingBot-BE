from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Text
from os import environ, path
from dotenv import load_dotenv
from db import db
from ma import ma
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


from models.user import User
from models.recipe import Recipe
from schemas.user import UserSchema, user_schema, users_schema
from schemas.recipe import Recipe, recipe_schema, recipes_schema
load_dotenv()

application = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
application.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')


db.init_app(application)
ma.init_app(application)
jwt = JWTManager(application)


'''
test data
'''

@application.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB created')


@application.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped')


@application.cli.command('db_seed')
def db_seed():
    fish_tacos = Recipe(recipe_name='Fish tacos', recipe_description='Delicios fish tacos from Tijuana', meal='Always', time=25, ingredients='fish and torillas', instructions='Fry everything together and hope for the best')
    chicken_katsu = Recipe(recipe_name='Chicke Katsu', recipe_description='The best chicken katsu', meal='Always', time=25, ingredients='Chiken and katsu curry', instructions='order online from cocoro on delivroo, must me in Kentish')

    db.session.add(fish_tacos)
    db.session.add(chicken_katsu)

    test_user = User(name='William', email='test@test.com', password='Password')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')


@application.before_first_request
def create_tables():
    db.create_all()


# Endpoints

# User
@application.route('/')
def landing():
    return 'signup or login'


@application.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email is already in use, please log in'), 409
    else:
        name = request.form['name']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message=f'Welcome aboard {name} 👩‍🍳'), 201


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='login successful', access_token=access_token)
    else:
        return jsonify(message='bad email or password'), 401


# Add retrieve password at some point


# Recipes

@application.route('/recipes', methods=['GET'])
def recipes():
    recipes_list = Recipe.query.all()  #please fix this for the love of god
    result = recipes_schema.dump(recipes_list)
    return jsonify(result)


#should this be by id? user will not query by id
@application.route('/recipe_details/<string:recipe_name>')
def recipe_details(recipe_name: String):
    recipe = Recipe.query.filter_by(recipe_name).first()
    if recipe:
        result = recipe_schema.dumop(recipe)
        return jsonify(result)
    else:
        return jsonify(message='That recipe has not been saved yet'), 404


#can the recipes be associated with each user?
@application.route('/add_recipe', methods=['GET', 'POST'])
@jwt_required
def add_recipe():
    recipe_name = request.form['recipe_name']
    test = Recipe.query.filter_by(recipe_name=recipe_name).first()
    if test:
        return jsonify('You already have a recipe with that name in your recipes'), 409
        # this should alos display the recipe that matches the name or similar
    else:
        recipe_name = request.form['recipe_name']
        recipe_description = request.form['recipe_description']
        meal = request.form['meal']
        time = float(request.form['time'])
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipe(recipe_name=recipe_name, recipe_description=recipe_description, meal=meal, time=time, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify(message='You added a recipe'), 201


@application.route('/update_recipe', methods=['GET', 'PUT'])
@jwt_required
def update_recipe():
    recipe_name = str(request.form['recipe_name'])
    recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
    if recipe:
        recipe.recipe_name = request.form['recipe_name']
        recipe.recipe_description = request.form['recipe_type']
        recipe.meal = request.form['meal']
        recipe.time = float(request.form['time'])
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        return jsonify(message=f'{recipe.recipe_name} created'), 202
    else:
        return jsonify(message='that recipe does not exist'), 404


if __name__ == '__main__':   
    application.run()  