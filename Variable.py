class Variable:

    def __init__(self, tipo, nombre=None, long=None, isEstructura=False):
        self.tipo = tipo
        self.nombre = nombre
        self.arrayLong = long
        self.isEstructura = isEstructura

    def getTipo(self):
        return self.tipo

    def __repr__(self):
        return f"<Variable> | tipo ={self.tipo} | arrayLong = {self.arrayLong} | isEstructura = {self.isEstructura}"
