from flask import Flask, render_template, request, redirect, url_for
from contacto import Contacto
from basededatos import agregar_toma, mostrar_contactos, consultar_contacto, actualizar_contacto, eliminar_contacto, agregar_dinero, mostrar_dinero
import json




app = Flask(__name__)

@app.route('/principal')
def principal():    
    return render_template('principal.html')

@app.route('/agregar_nueva_toma', methods=['GET', 'POST'])
def agregar_nueva_toma():    
    if request.method == 'POST':
        if request.form['submit_button'] == 'Guardar':
            nuevo_contacto = Contacto(request.form['nombre'])        
            nuevo_contacto.direccion=request.form['direccion']
            nuevo_contacto.numero_de_medidor=request.form['numero_de_medidor']
            nuevo_contacto.medida_actual=request.form['medida_anterior']
            nuevo_contacto.medida_actual=''  
            nuevo_contacto.adeudo=''
            nuevo_contacto.periodo='' 
            nuevo_contacto.fecha_ultimo_abono=''    
            usuario=nuevo_contacto.obtenerDatos()
            agregar_toma(usuario)
            return render_template('principal.html')
        #return json.dumps(usuario)
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
        
    elif request.method == 'GET':
        return render_template('agregar_nueva_toma.html')

@app.route('/mostrar_usuarios', methods=['GET', 'POST'])
def mostrar_usuario():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Inicio':
            return render_template('principal.html')
    if request.method == 'GET':
        contactos = mostrar_contactos()
        return render_template ('mostrar.html', contactos=contactos)

@app.route('/consultar_usuario',methods=['GET', 'POST'])
def consultar_usuario():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Consultar':
            consulta = consultar_contacto(request.form['numero_de_medidor'])
            todos = mostrar_contactos()
            return render_template ('buscar.html', consulta=consulta, todos=todos)
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
    elif request.method == 'GET':
        todos=mostrar_contactos()
        consulta={}
        return render_template ('buscar.html',consulta=consulta, todos=todos)



