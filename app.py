from flask import Flask , jsonify, request
import json
app = Flask (__name__)

productos= []


@app.route('/ping', methods= ['GET'])
def ping():
    return jsonify({'mensaje':'pong!'})

# PONES MENSAJE DENTRO DEL JSON

@app.route('/productos', methods= ['GET'])
def getproductos():
    with open('productos.json', 'r') as file:
        productos = json.load(file)
    return jsonify({"Poductos": productos, "mensajes": "productos"}),200

# buscar por nombre 

@app.route('/productos/<string:producto_nombre>', methods= ['GET'])
def getproducto(producto_nombre):
    producfoud=[producto for producto in productos if producto['nombre']== producto_nombre]
    if (len (producfoud) >0):
        return jsonify({"el producto los encontramos":producfoud}),200
    return jsonify({"mensaje ": "no se encontro el producto"}),404
      
#Ruta para crear datos

import os

@app.route('/productos', methods=['POST'])
def addproductos():
    agregando = request.json
    archivo = 'productos.json'
    
    with open(archivo, 'r') as file:
        productos = json.load(file)

    productos.append(agregando)

    with open(archivo, 'w') as file:
        json.dump(productos, file, indent=4)

    return jsonify({"mensaje": "Todo created successfully", "lista actualizada: ": productos})

#actualizar datos

@app.route('/productos/<string:producto_nombre>', methods= ['PUT'])
def update_productos(producto_nombre):
    with open('productos.json', 'r') as file:
        productos = json.load(file)
    index_prod=[producto for producto in productos if producto['nombre']== producto_nombre]
    if (len(index_prod)> 0):
        index_prod[0]['nombre'] = request.json['nombre']
        index_prod[0]['precio'] = request.json['precio']
        index_prod[0]['cantidad'] = request.json['cantidad']
        with open('productos.json', 'w') as file:
            json.dump(productos, file, indent=4)
        return jsonify({"mensaje": "Producto actualizado", "producto": index_prod[0]})
    return jsonify({"mensaje": "No se encontró el producto"}), 404


#borrar datos


@app.route('/productos/<string:producto_nombre>', methods=['DELETE'])
def delete_producto(producto_nombre):
    with open('productos.json', 'r') as file:
        productos = json.load(file)
    for producto in productos:
        if producto['nombre'] == producto_nombre:
            productos.remove(producto)
            with open('productos.json', 'w') as file:
                json.dump(productos, file, indent=4)
            return jsonify({"mensaje": "Producto eliminado", "productos restantes": productos})
    return jsonify({"mensaje": "No se encontró el producto"}), 404





if __name__ == '__main__':
    app.run(debug=True, port= 5000)


