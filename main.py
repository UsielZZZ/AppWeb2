#importacion de librerias
from flask import Flask, render_template, request, redirect, url_for

import psycopg2
from flask_sqlalchemy import SQLAlchemy

from flaskext.mysql import MySQL

#creacion de objeto de flask


app = Flask(__name__, static_url_path='/static')

#conexion de MySQL



db = SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-3-218-149-60.compute-1.amazonaws.com",
    database="da1uoqns6u9nsp",
    user="usalpkvauufkls",
    password="678f01983e90425880fded20d682bf1b7317270de5b5873b2e27a98e9b843297"
)


#creamos una ruta raiz de la pagina principal
@app.route("/")

#Creacion de funcion para renderizar index
def index():

    return render_template("index.html")

@app.route("/rejilla")
def rejilla_html():
    return render_template("html_rejilla.html")

@app.route("/formulario")
def formulario():

    conexion = conn.cursor()
    conexion.execute("SELECT * from registro")
    datos= conexion.fetchall()
    print(datos)
    conexion.close()
    return render_template("formulario.html", productos=datos)

@app.route("/guardar_info", methods=["POST"])
def guardar_info():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    usuario = request.form["usuario"]

    sexo = request.form["sexo"]
    contra = request.form["contra"]


    cursor = conn.cursor()

    cursor.execute("INSERT INTO registro(nombre, correo, usuario, sexo, contra) values (%s, %s, %s, %s, %s)", (nombre, correo, usuario, sexo, contra))
    conn.commit()
    cursor.close()
    return redirect("/formulario")

@app.route("/eliminar_producto/<string:usuario>")
def eliminar_producto(usuario):


    cursor = conn.cursor()

    cursor.execute("delete from registro where usuario='"+usuario+"'")

    conn.commit()
    cursor.close()
    return redirect("/formulario")

@app.route("/consultar_producto/<string:usuario>")
def consultar_producto(usuario):


    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registro where usuario='"+usuario+"'")
    dato = cursor.fetchone()
    print(dato)
    cursor.close()
    return render_template("editar_producto.html", producto=dato)


@app.route("/editar_producto/<string:usuario>", methods=["POST"])
def editar_producto(usuario):

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    sexo = request.form["sexo"]
    contra = request.form["contra"]


    cursor = conn.cursor()
    cursor.execute("UPDATE registro SET nombre=%s, sexo=%s, contra=%s", (nombre, sexo, contra))
    conn.commit()
    cursor.close()
    return redirect("/formulario")



#Configuracion principal de archivo de ejecucion
if __name__ == '__main__':
    #configuracion de puerto de escucha del servidor web
    app.run(port = 80, debug = True)

