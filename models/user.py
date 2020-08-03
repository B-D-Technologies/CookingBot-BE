from db import db
from sqlalchemy import Column, Integer, String, Float, Text


class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

