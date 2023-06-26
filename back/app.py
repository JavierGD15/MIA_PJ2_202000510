from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route('/interpretar', methods=['POST'])
def consola():
    comando= request.get_json()
    for key in comando['entrada'].splitlines():
        print(key)
    return jsonify({'salida': str(comando['entrada'])})

@app.route('/login', methods=['POST'])
def login():
    comando= request.get_json()
    user = comando['usuario']
    password = comando['password']
    print(user)
    print(password)
    resolucion = False
    return jsonify({'salida': str(resolucion)})

if __name__ == '__main__':
    app.run(port=8000, debug=True)