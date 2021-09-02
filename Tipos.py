from Error import *


def procesarExp(exp):
    '''
    Funcion para validar los tipos de una expresion.

    Parametros
    - expresion: lista de tipos de datos Ej: ['boolOp', 'boolean', 'boolean']
    '''
    exp.reverse()

    print(f'''
            Exp {exp}
            ''')
    if (len(exp) == 1):
        return exp.pop()
    operadores = ['intOp', 'relOp', 'eqOp', 'boolOp', 'negative', 'not']
    pila = []
    for i in exp:
        if i not in operadores:
            # no es operador
            pila.append(i)
        else:
            # es operador

            # relga not
            if (i == 'not'):
                if (pila.pop() == 'boolean'):
                    pila.append('boolean')
                else:
                    pila.append('err')
                continue
            # relga negative
            if (i == 'negative'):
                if (pila.pop() == 'int'):
                    pila.append('int')
                else:
                    pila.append('err')
                continue

            # regla intOp
            if (i == 'intOp'):
                if (pila.pop() == pila.pop() == 'int'):
                    pila.append('int')
                else:
                    pila.append('err')
                continue

            # regla mayor, menor
            if (i == 'relOp'):
                if (pila.pop() == pila.pop() == 'int'):
                    pila.append('boolean')
                else:
                    pila.append('err')
                continue

            # regla ==, !=
            if (i == 'eqOp'):
                if (pila.pop() == pila.pop() != 'err'):
                    pila.append('boolean')
                else:
                    pila.append('err')
                continue

            # regla &&, ||
            if (i == 'boolOp'):
                if (pila.pop() == pila.pop() == 'boolean'):
                    pila.append('boolean')
                else:
                    pila.append('err')
                continue

    return pila.pop()


def getMethodType(nombre, pilaFuncion):
    '''
    Funcion para obtener el tipo de una funcion.
    Valida si la funcion ya fue declarada dentro del ambito.

    Parametros
    - nombre: nombre de la funcion
    - pilaFuncion: pila de ambitos de las funciones

    Retornos
    - <Error> si la funcion no se encuentra en los ambitos
    - tipo en el caso de que se encuentre la funcion
    '''
    for ambito in pilaFuncion:
        if(nombre in ambito.keys()):
            return ambito[nombre].tipo

    return Error('La funcion no existe')
