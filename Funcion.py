class Funcion:
    def __init__(self, tipo, argumentos=[], retorno=[]):
        self.tipo = tipo
        self.argumentos = argumentos
        self.retorno = retorno
        self.err = None
        self.validar()

    def validarRetorno(self):
        control = self.retorno[0]
        for i in self.retorno:
            if (i != control):
                return None
        return control

    def validar(self):
        print(self)
        if (self.tipo == 'void'):
            if(len(self.retorno) > 0):
                self.err = 'Funcion void no retorna nada'
        else:
            if(len(self.retorno) == 0):
                self.err = 'Falta retorno de funcion'
            else:
                if(self.tipo != self.validarRetorno()):
                    print(self.tipo)
                    print(self.validarRetorno())
                    self.err = 'El tipo de la funcion y el tipo de retorno no coinciden'

    def __repr__(self):
        return f"<Funcion>{self.tipo}({self.argumentos}): {self.retorno}"
