class Variable:

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def getTipo(self):
        return self.tipo

    def __repr__(self):
        return f"<Variable>{self.tipo}:{self.nombre}"
