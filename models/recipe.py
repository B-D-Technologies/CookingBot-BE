from db import db
from sqlalchemy import Column, Integer, String, Float, Text


class Recipe(db.Model):
    recipe_id = Column(Integer, primary_key=True, unique=True)
    recipe_name = Column(String(50), unique=True)
    recipe_description = Column(String)
    meal = Column(String)
    time = Column(Float)
    ingredients = Column(String(30)) #How can the user add more
    instructions = Column(String(150)) #How can the user add mode?