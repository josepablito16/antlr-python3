class Funcion:
    def __init__(self, tipo, argumentos=[], retorno=[]):
        self.tipo = tipo
        self.argumentosTipos = argumentos  # array solo tipos
        self.retornoTipos = retorno  # array solo tipos
        self.err = None
        self.validar()

    def validarRetorno(self):
        control = self.retornoTipos[0]
        for i in self.retornoTipos:
            if (i != control):
                return None
        return control

    def validar(self):
        print(self)
        if (self.tipo == 'void'):
            if(len(self.retornoTipos) > 0):
                self.err = 'Funcion void no retorna nada'
        else:
            if(len(self.retornoTipos) == 0):
                self.err = 'Falta retorno de funcion'
            else:
                if(self.tipo != self.validarRetorno()):
                    self.err = 'El tipo de la funcion y el tipo de retorno no coinciden'

    def __repr__(self):
        return f"<Funcion>{self.tipo}({self.argumentosTipos}): {self.retornoTipos}"
