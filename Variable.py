class Variable:

    def __init__(self, tipo, nombre=None, long=None):
        self.tipo = tipo
        self.nombre = nombre
        self.arrayLong = long

    def getTipo(self):
        return self.tipo

    def __repr__(self):
        return f"<Variable>{self.tipo}:{self.nombre}"
