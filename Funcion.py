from Error import *


class Funcion:
    def __init__(self, tipo, argumentos=[], retorno=[]):
        self.tipo = tipo
        self.argumentosTipos = argumentos  # array solo tipos
        self.retornoTipos = retorno  # array solo tipos
        self.err = None

    def validarRetorno(self):
        control = self.retornoTipos[0]
        for i in self.retornoTipos:
            if (i != control):
                return None
        return control

    def agregarReturn(self, tipo=None):
        """
        print(f''' 
        agegarReturn 
        tipo {tipo}
        retornoTipos {self.retornoTipos}
        ''')
        """
        self.retornoTipos.append(tipo)

    def validar(self):
        """
        print(f'''
        -----
        validar
        -----
        {self.tipo}
        {self.retornoTipos}
        ''')
        """
        if (self.tipo == 'void'):
            if(len(self.retornoTipos) > 0):
                self.err = Error('Funcion void no retorna nada')
        else:
            if(len(self.retornoTipos) == 0):
                self.err = Error('Falta retorno de funcion')
            else:
                if(self.tipo != self.validarRetorno()):
                    self.err = Error(
                        'El tipo de la funcion y el tipo de retorno no coinciden')

    def __repr__(self):
        return f"<Funcion>{self.tipo}({self.argumentosTipos}): {self.retornoTipos}"
