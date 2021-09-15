class Nodo:

    def __init__(self, tipo, nombre):
        self.tipo = tipo  # Tipo de dato
        self.nombre = nombre  # Nombre del nodo donde retornamos el valor

    def __repr__(self):
        return f"<Nodo>{self.tipo} {self.nombre}"
