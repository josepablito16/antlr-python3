class Nodo:

    def __init__(self, tipo, nombre=None, isArray=None, direccion=None, siguiente=None, etiquetaTrue=None, etiquetaFalse=None):
        self.tipo = tipo  # Tipo de dato
        self.nombre = nombre  # Nombre del nodo donde retornamos el valor
        self.isArray = isArray
        self.direccion = direccion
        self.codigo = []
        self.siguiente = siguiente
        self.etiquetaTrue = etiquetaTrue
        self.etiquetaFalse = etiquetaFalse

    def __repr__(self):
        return f"<Nodo>{self.tipo} {self.nombre}"
