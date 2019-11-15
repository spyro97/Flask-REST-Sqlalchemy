import pyodbc
import json
import urllib
import os
import requests
from flask import Flask, jsonify, request, render_template
from extensions import db
from urls import blueprint_urls


app = Flask(__name__)

databse_uri = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+13+for+SQL+Server%7D%3BServer%3D172.16.1.108%3BDatabase%3Dprueba%3BUID%3Dsa%3BPWD%3DDsdsistemas2012%3BPort%3D1433%3BTrusted_Connection%3Dno%3B'
app.config["SQLALCHEMY_DATABASE_URI"] = databse_uri

app.register_blueprint(blueprint_urls)
db.init_app(app)
print(db)
