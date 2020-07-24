class Contacto:

    def __init__(self, info):
        if isinstance(info, str):
            self.nombre = info
            self.direccion = ""
            self.numero_de_medidor = ""
            self.medida_anterior = ""
            self.medida_actual = ""
            self.adeudo = ""
            self.periodo = ""
            self.fecha_ultimo_abono = ""
        elif isinstance(info, dict):
            self.nombre = info['nombre']
            self.direccion = info['direccion']
            self.numero_de_medidor = info['numero_de_medidor']
            self.medida_anterior = info['medida_anterior']
            self.medida_actual = info['medida_actual']
            self.adeudo = info['adeudo']
            self.periodo = info['periodo']
            self.fecha_ultimo_abono = info['fecha_ultimo_abono']
        else:
            raise TypeError

    def obtenerDatos(self):
        return self.__dict__