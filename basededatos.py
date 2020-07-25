from pymongo import MongoClient

cliente = MongoClient('localhost', 27017)
#db = cliente.ejemplo_pymongo
#coleccion = db.prueba
db = cliente['aguapotable']
#db = cliente.ejemplo
coleccion = db.datos
dinero = db.datos

def agregar_dinero(informacion):
    id = dinero.insert_one(informacion)
    return id

def mostrar_dinero():
    extras = dinero.find()
    return list(extras)

def agregar_toma(registros):
    id = coleccion.insert_one(registros)
    return id

def mostrar_contactos():
    cursor = coleccion.find()
    return list(cursor)

def consultar_contacto(titulo):
    resultado = coleccion.find_one({'numero_de_medidor': titulo})
    return resultado

def actualizar_contacto(numero_de_medidor, registros):
    resultado = coleccion.update_one({'numero_de_medidor': numero_de_medidor}, 
        {'$set': {'nombre': registros['nombre'],'direccion':registros['direccion'],'numero_de_medidor':registros['numero_de_medidor'],'medida_anterior':registros['medida_anterior'],'medida_actual':registros['medida_actual'],'adeudo':registros['adeudo'],'periodo':registros['periodo'],'fecha_ultimo_pago':registros['fecha_ultimo_pago'],'adeudo_anterior':registros['adeudo_anterior'],'abono':registros['abono']}})
    return str(resultado.modified_count)

def eliminar_contacto(titulo):
    resultado= coleccion.delete_one({'numero_de_medidor': titulo})
    return resultado.deleted_count