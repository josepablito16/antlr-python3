class Funcion:
    def __init__(self, tipo, argumentos=[], retorno=[]):
        self.tipo = tipo
        self.argumentosTipos = argumentos  # array solo tipos
        self.retornoTipos = retorno  # array solo tipos
        self.retornoTemp = []
        self.err = None

    def validarRetorno(self):
        control = self.retornoTipos[0]
        for i in self.retornoTipos:
            if (i != control):
                return None
        return control

    def agregarReturn(self, tipo=None):
        if(tipo):
            #print('agregarReturn con tipo')
            self.retornoTipos.append(tipo)
        else:
            #print('agregarReturn sin tipo')
            self.retornoTipos.append(self.retornoTemp.pop())

    def procesarReturn(self, retornoArray):

        valorTemp = None
        operadorTemp = None

        condicionRepetir = len(retornoArray) == 4
        if (condicionRepetir):
            self.retornoTemp.append(retornoArray.pop(0))
        elif(len(retornoArray) == 2 and len(self.retornoTemp) > 0):
            retornoArray = self.retornoTemp + retornoArray
            self.retornoTemp.clear()

        print(f'''
        -----
        procesarReturn
        -----
        retornoArray {retornoArray}
        retornoTemp {self.retornoTemp}
        ''')

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

        if condicionRepetir:
            retornoArrayNuevo = []
            retornoArrayNuevo += self.retornoTemp
            retornoArrayNuevo.append(valorTemp)
            self.retornoTemp = []
            self.procesarReturn(retornoArrayNuevo)
        else:
            self.retornoTemp.append(valorTemp)
            print(f'valorTemp {valorTemp}')

    def validar(self):
        print(f'''
        -----
        validar
        -----
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
