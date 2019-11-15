from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from api import db
import os


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self,username, email):
        self.username = username
        self.email = email

    #Schema Product
    
    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
 
