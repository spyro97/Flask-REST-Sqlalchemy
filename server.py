import pyodbc
import json
import urllib
import os
import requests
from flask import Flask, jsonify, request, render_template
from products import products
from extensions import db
from urls import blueprint_urls


app = Flask(__name__)

databse_uri = 'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+13+for+SQL+Server%7D%3BServer%3D172.16.1.108%3BDatabase%3Dprueba%3BUID%3Dsa%3BPWD%3DDsdsistemas2012%3BPort%3D1433%3BTrusted_Connection%3Dno%3B'
app.config["SQLALCHEMY_DATABASE_URI"] = databse_uri

'''class User(db.Model):
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
'''




@app.route("/users/<id>", methods=['PUT'])
def modifly_user(id):
    #from models.models import User
    user = User.query.get(id)
    print(user.to_json())
    data = {
        "username": request.json['username'],
        "email": request.json['email']
    }
    user.email = data["email"]
    user.username = data["username"]
    db.session.add(user)
    db.session.commit()
    print(user.email)
    print(user.username)
    return jsonify({"message": user.to_json()})

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": user.to_json()})



@app.route("/productsdb", methods=['GET'])
def read2():
    print("Lectura")
    data = []
    cursor = conn.cursor()
    cursor.execute("select * from productos")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'id_Producto': row[0], 'producto': row[1], 'descripcion': row[2], 'precio': row[3], 'stock': row[4]})
    return jsonify(data)
    return jsonify({"message": "There are no products to show"})

#Obtener producto especifico de la base de datos
@app.route("/productsdb/<int:product_id>", methods=['GET'])
def read3(product_id):
    data = []
    cursor = conn.cursor()
    cursor.execute(
        "select * from productos where id_Producto = ?",
        (product_id)
        )
    rows = cursor.fetchall()
    for row in rows:
        data.append(
            {'id_Producto': row[0], 'producto': row[1], 
             'descripcion': row[2], 'precio': row[3], 'stock': row[4]}
            )
        return jsonify(data)
    return jsonify({"message": "The product doesn´t exist in the database"})

#Insertar productos en la base de datos
@app.route("/productsdb", methods=['POST'])
def insert():
    newProduct = {
        "id_Producto": request.json['id_Producto'],
        "producto": request.json['producto'],
        "descripcion": request.json['descripcion'],
        "precio": request.json['precio'],
        "stock": request.json['stock'],
        }
    cursor = conn.cursor()
    cursor.execute(
        'insert into productos (id_Producto, producto, descripcion, precio, stock) values (?,?,?,?,?)',
        (newProduct["id_Producto"], newProduct["producto"],newProduct["descripcion"], newProduct["precio"], newProduct["stock"])
        )
    conn.commit()
    return read2()

#Editar productos
@app.route("/productsdb/<int:product_id>", methods=['PUT'])
def editProduct(product_id):
    if(product_id > 0 ):
        productFound = {
        "producto": request.json['producto'],
        "descripcion": request.json['descripcion'],
        "precio": request.json['precio'],
        "stock": request.json['stock'],
    }
    cursor = conn.cursor()
    cursor.execute(
        'update productos set producto=?, descripcion=?, precio=?, stock=? where id_Producto=?',
        (productFound["producto"],productFound["descripcion"], productFound["precio"], productFound["stock"], product_id)
        )
    conn.commit()
    return read2()

#Eliminar producto
@app.route("/productsdb/<int:product_id>", methods=['DELETE'])
def deleteProduct(product_id):
    cursor = conn.cursor()
    cursor.execute('delete from productos where id_Producto=?;',
                  (product_id)
                  )
    conn.commit()
    return read2()


#Visualizar index
@app.route('/view')
def hello_world():
    titulo = "GeekyFlask"
    users = [{"nombre": "Bryan"},{"nombre": "Hiram"},{"nombre": "Luna"}]
    usuario = {'nombre': 'Alejandro'}
    return render_template('index.html',
        titulo=titulo,
        usuario=usuario,
        usuarios=users
        )

app.register_blueprint(blueprint_urls)
db.init_app(app)
print(db)
