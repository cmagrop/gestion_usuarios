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
@app.route("/usuarios/crear", methods=["POST"])
def crear():
    data ={
        "nombre":request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email']
    }
    query= "insert into usuarios (nombre,apellido,email,created_at,updated_at) " \
    "values(%(nombre)s,%(apellido)s,%(email)s,NOW(),NOW())"
    #conexion a la BD->creando un objeto de tipo MySQLConnection
    mysql = connectMySQL('esquema_usuarios')
    #Guardar , se devolverá el id del usuario creado
    nuevo_id = mysql.query_db(query,data)
    #redirigir a la pagina principal
    return redirect(f'/{nuevo_id}')
#Ruta para mostrar la informacion detallada de un usuario
@app.route("/<int:id>")
def mostrar_usuario(id):
    query = "select * from usuarios where id=%(id)s"
    data = {"id":id}
    #conexion a la BD
    mysql = connectMySQL('esquema_usuarios')
    #resultado es una lista con todos los resultados, donde en este caso
    #el resultado solo será el correspondiente al id consultado
    resultado = mysql.query_db(query,data) #obtener resultados
    if not resultado: #que si no existen resultados
        return redirect("/")
    return render_template('mostrar.html',usuario=resultado[0])  
#usuario=['Marta']
#mostrar la vista del formulario para llenado de campos
@app.route("/<int:id>/editar")
def editar(id):
    query = "select * from usuarios where id=%(id)s"
    data = {"id":id}
    mysql = connectMySQL("esquema_usuarios")
    resultado = mysql.query_db(query,data)
    if not resultado:
        return redirect("/")
    return render_template("editar.html",usuario=resultado[0])

#ruta de formulario actualización
@app.route("/usuarios/<int:id>/actualizar", methods=['POST'])
def actualizar(id):
    data ={
            "nombre":request.form['nombre'],
            "apellido": request.form['apellido'],
            "email": request.form['email']
        }
    query= "update usuarios set nombre=%(nombre)s,apellido=%(apellido)s,email=%(email)s" \
    "updated_at=NOW() where id=%(id)s"
        #conexion a la BD
    mysql = connectMySQL('esquema_usuarios')
    mysql.query_db(query,data) #ejecuta la consulta
    return redirect(f'/{id}')
    

       


if __name__ == '__main__':
    app.run(debug=True)                           