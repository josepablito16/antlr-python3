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

    def agregarReturn(self, retornoArray):
        print(retornoArray)
        valorTemp = None
        operadorTemp = None
        for i in range(len(retornoArray)):
            if (i % 2 == 0):
                # valor
                if (operadorTemp):
                    # hay operador
                    '''
                    intOp
                    relOp
                    eqOp
                    boolOp
                    '''

                    # regla int
                    if (valorTemp == 'int' and operadorTemp == 'intOp' and retornoArray[i] == 'int'):
                        valorTemp = 'int'
                        operadorTemp = None

                    # regla mayor, menor
                    elif (valorTemp == 'int' and operadorTemp == 'relOp' and retornoArray[i] == 'int'):
                        valorTemp = 'boolean'
                        operadorTemp = None

                    # regla ==, !=
                    elif ((valorTemp == retornoArray[i] != 'err') and operadorTemp == 'eqOp'):
                        valorTemp = 'boolean'
                        operadorTemp = None

                    # regla &&, ||
                    elif (valorTemp == 'boolean' and operadorTemp == 'boolOp' and retornoArray[i] == 'boolean'):
                        valorTemp = 'boolean'
                        operadorTemp = None

                    else:
                        valorTemp = 'err'
                else:
                    # No Hay operador
                    valorTemp = retornoArray[i]
            else:
                # operador
                operadorTemp = retornoArray[i]

        self.retornoTipos.append(valorTemp)
        print(valorTemp)

    def validar(self):
        print(f'''
        {self.tipo}
        {self.retornoTipos}
        ''')
        if (self.tipo == 'void'):
            if(len(self.retornoTipos) > 0):
                self.err = 'Funcion void no retorna nada'
        else:
            if(len(self.retornoTipos) == 0):
                print(len(self.retornoTipos))
                self.err = 'Falta retorno de funcion'
            else:
                if(self.tipo != self.validarRetorno()):
                    self.err = 'El tipo de la funcion y el tipo de retorno no coinciden'

    def __repr__(self):
        return f"<Funcion>{self.tipo}({self.argumentosTipos}): {self.retornoTipos}"
