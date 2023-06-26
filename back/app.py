from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
from Pantallas.Admin import Application
from Pantallas.encriptado import desencriptar


app = Flask(__name__)
CORS(app)

@app.route('/interpretar', methods=['POST'])
def consola():
    comando= request.get_json()
    usos = Application()
    usos.ejecutar(comando['entrada'])
    return jsonify({'salida': str(comando['entrada'])})

@app.route('/login', methods=['POST'])
def login():
    comando= request.get_json()
    user = str(comando['usuario'])
    password = str(comando['password'])
    registro = desencriptar(b'miaproyecto12345')
    if registro.leer_archivo(user,password) == True:
        resolucion = True
        return jsonify({'salida': str(resolucion)})
    else:
        resolucion = False
        return jsonify({'salida': str(resolucion)})

if __name__ == '__main__':
    app.run(port=8000, debug=True)