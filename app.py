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
            nuevo_contacto.medida_anterior=request.form['medida_anterior']
            nuevo_contacto.medida_actual=request.form['medida_anterior'] 
            nuevo_contacto.adeudo='0'
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
            consulta = consultar_contacto(request.form['numerodemedidor'])
            todos = mostrar_contactos()
            return render_template ('buscar.html', consulta=consulta, todos=todos)
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
    elif request.method == 'GET':
        todos=mostrar_contactos()
        consulta={}
        return render_template ('buscar.html',consulta=consulta, todos=todos)

@app.route('/eliminar',methods=['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Consultar':
            consulta = consultar_contacto(request.form['numerodemedidor'])
            todos = mostrar_contactos()
            return render_template ('eliminar.html', consulta=consulta, todos=todos)
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
        elif request.form['submit_button'] == 'Eliminar':
            consulta=eliminar_contacto(request.form['numero_de_medidor'])
            return render_template ('principal.html')
    elif request.method == 'GET':
        todos=mostrar_contactos()
        consulta={}
        return render_template ('buscar.html',consulta=consulta, todos=todos)

@app.route('/actualizar',methods=['POST','GET'])
def actualizar():
    if request.method == 'POST':  
        if request.form['submit_button'] == 'Consultar':
            consulta = consultar_contacto(request.form['numerodemedidor'])
            #todos = mostrar_contactos()
            return render_template ('actualizar.html', consulta=consulta)    
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
        elif request.form['submit_button'] == 'Actualizar':
            nuevo_contacto = {}
            nuevo_contacto['nombre']= request.form['nombre']
            nuevo_contacto['direccion']= request.form['direccion']
            nuevo_contacto['numero_de_medidor']= request.form['numero_de_medidor']
            nuevo_contacto['medida_actual']= request.form['medida_actual']
            medidaactual=request.form['medida_actual']
            medidaanterior=request.form['medida_anterior']
            total=int (medidaactual) - int (medidaanterior)
            if total<100:
                deuda=total*1
            elif total<200:
                total=total-100
                deuda=(100*1)+total*2
            elif total>200:
                total=total-200
                deuda=300+total*5
            antes=int(request.form['adeudo'])
            nuevo_contacto['adeudo']= deuda+antes
            nuevo_contacto['periodo']=request.form['periodo']
            nuevo_contacto['fecha_ultimo_pago']=""
            nuevo_contacto['adeudo_anterior']="0"
            nuevo_contacto['abono']="0"
            nuevo_contacto['medida_anterior']= request.form['medida_anterior']
            
            consulta = actualizar_contacto(request.form['numero_de_medidor'],nuevo_contacto)
            todos = mostrar_contactos()
            return render_template ('actualizar.html',consulta=consulta, todos=todos)
    elif request.method == 'GET':
        todos=mostrar_contactos()
        consulta={}
        return render_template ('actualizar.html',consulta=consulta, todos=todos)

@app.route('/pagar',methods=['POST','GET'])
def pagar():
    if request.method == 'POST':  
        if request.form['submit_button'] == 'Consultar':
            consulta = consultar_contacto(request.form['numerodemedidor'])            
            return render_template ('pagar.html', consulta=consulta)    
        elif request.form['submit_button'] == 'Inicio':
            return render_template ('principal.html')
        elif request.form['submit_button'] == 'Pagar':
            nuevo_contacto = {}
            nuevo_contacto['nombre']= request.form['nombre']
            nuevo_contacto['direccion']= request.form['direccion']
            nuevo_contacto['numero_de_medidor']= request.form['numero_de_medidor']
            nuevo_contacto['medida_anterior']= request.form['medida_anterior']            
            nuevo_contacto['medida_actual']=request.form['medida_actual']            
            nuevo_contacto['periodo']=request.form['periodo']
            abono=int(request.form['abono'])
            anterior=int(request.form['adeudo_anterior'])
            total=anterior-abono
            nuevo_contacto['adeudo']=total
            nuevo_contacto['adeudo_anterior']=anterior
            nuevo_contacto['fecha_ultimo_pago']=request.form['fecha_ultimo_pago']
            nuevo_contacto['abono']=abono                
            #en_caja=mostrar_dinero()
            #guardado=en_caja['dinero_en_caja']                     
            consulta = actualizar_contacto(request.form['numero_de_medidor'],nuevo_contacto)
            todos = mostrar_contactos()
            return render_template ('actualizar.html',consulta=consulta, todos=todos)
        elif request.form['submit_button'] == 'Imprimir_comprobantes':
            consulta = mostrar_contactos()
            return render_template ('comprobantes.html', consulta=consulta)
    elif request.method == 'GET': 
        todos=mostrar_contactos()
        consulta={}
        return render_template ('actualizar.html',consulta=consulta, todos=todos)

