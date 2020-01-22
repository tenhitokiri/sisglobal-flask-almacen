from flask import Flask, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import os

# iniciar App
app = Flask(__name__)

# Conexiones a DB
app.config['MYSQL_HOST'] = '10.1.1.32'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '4c3r04dm1n'
app.config['MYSQL_DB'] = 'intranet'

# Otras variables
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'estaeslaclavesecreta'
mysql = MySQL(app)

# Rutas
@app.route('/')
def inicio():
    return "hola"


@app.route('/almacen/', methods=['GET'])
def almacenes():
    cur = mysql.connection.cursor()
    cur.execute('select * from adm_almacen')
    almacenes = cur.fetchall()
    resultado = []
    for almacen in almacenes:
        almacen_datos = {}
        almacen_datos['id_almacen'] = almacen[0]
        almacen_datos['cod_almacen'] = almacen[1]
        almacen_datos['nombre'] = almacen[2]
        almacen_datos['descripcion'] = almacen[3]

        cur2 = mysql.connect.cursor()
        cur2.execute(
            'select * from adm_almacen_piso where idAlmacen = {0}'.format(almacen[0]))
        pisos = cur2.fetchall()
        resultado_pisos = []
        for piso in pisos:
            piso_datos = {}
            piso_datos['id_piso'] = int(piso[0])
            piso_datos['descripcion_piso'] = piso[1]
            piso_datos['id_almacen_piso'] = piso[2]
            resultado_pisos.append(piso_datos)

        almacen_datos['pisos'] = resultado_pisos
        resultado.append(almacen_datos)
    return jsonify(resultado)


@app.route('/pisos/<int:id>', methods=['GET'])
def pisos_almacenes(id):
    cur2 = mysql.connect.cursor()
    cur2.execute(
        'select * from adm_almacen_piso where idAlmacen = {0}'.format(id))
    pisos = cur2.fetchall()
    resultado_pisos = []
    for piso in pisos:
        piso_datos = {}
        piso_datos['id_piso'] = piso[0]
        piso_datos['descripcion_piso'] = piso[1]
        piso_datos['id_almacen_piso'] = piso[2]
        resultado_pisos.append(piso_datos)
    return jsonify(resultado_pisos)


if __name__ == '__main__':
    app.run(debug=True)
