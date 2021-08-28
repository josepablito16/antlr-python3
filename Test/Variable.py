class Variable:

    def __init__(self, tipo, nombre=None):
        self.tipo = tipo
        self.nombre = nombre

    def getTipo(self):
        return self.tipo

    def __repr__(self):
        return f"<Variable>{self.tipo}:{self.nombre}"
