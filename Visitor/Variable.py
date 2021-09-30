class Variable:

    def __init__(self, tipo, nombre=None, long=None, isEstructura=False, offset=None, local=None):
        self.tipo = tipo
        self.nombre = nombre
        self.arrayLong = long  # longitud del array
        self.isEstructura = isEstructura
        self.offset = offset
        self.isLocal = local

    def getTipo(self):
        return self.tipo

    def __repr__(self):
        return f"<Variable> | tipo ={self.tipo} | arrayLong = {self.arrayLong} | isEstructura = {self.isEstructura} | offset = {self.offset} | isLocal = {self.isLocal} \n"
