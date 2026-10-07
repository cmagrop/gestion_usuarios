from flask import Flask,render_template,request,redirect
from mysqlconnection import connectMySQL
"""
Flask: importación de Flask
render_template: dibujar en pantalla lo que deseamos mostrar
request: solicitar consultas desde lo mando el navegador(cliente) 
redirect: redireccionar una pagina
"""
app = Flask(__name__) #crea una app de Flask 
#donde tome app.py como un modulo independiente
#1. Ruta para ver a todos los usuarios
@app.route("/")
def index():
    #objeto de una conexion  MySQL
    mysql = connectMySQL('esquema_usuarios')
    usuarios = mysql.query_db("select * from usuarios")
    return render_template('index.html',
                           todos_los_usuarios=usuarios)
#generar la ruta para el formulario de creación usuarios
@app.route("/usuarios/nuevo")
def nuevo():
    return render_template('nuevo.html')
#crear la ruta para procesar el formulario
#@app.route("/usuarios/crear")
#def crear():


if __name__ == '__main__':
    app.run(debug=True)                           