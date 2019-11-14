import pyodbc
import json
from flask import Flask, jsonify, request, render_template
from products import products

app = Flask(__name__)

#Conecion a la base de datos
conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=172.16.1.108;"
    "Database=prueba;"
    "UID=sa;"
    "PWD=Dsdsistemas2012"  
    )

#Obtener productos de la base de datos
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

#Ejecutar Servicio/Servidor
if __name__ == '__main__':
    app.run(debug=True, port=4000)



