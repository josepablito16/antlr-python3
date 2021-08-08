class Funcion:
    def __init__(self, tipo, argumentos=[], retorno=None):
        self.tipo = tipo
        self.argumentos = argumentos
        self.retorno = retorno
        self.err = None
        self.validar()

    def validar(self, regla=None):
        if (self.tipo == 'void'):
            if(self.retorno != None):
                self.err = 'Funcion void no retorna nada'
        else:
            if(self.retorno == None):
                self.err = 'Falta retorno de funcion'
            else:
                if(self.tipo != self.retorno.tipo):
                    self.err = 'El tipo de la funcion y el tipo de retorno no coinciden'

    def __repr__(self):
        return f"<Funcion>{self.tipo}({self.argumentos}): {self.retorno}"
