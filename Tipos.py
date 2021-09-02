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

    return Error(f'La funcion {nombre} no existe')


def getidLocationType(nombre, pilaVariable):
    '''
    Funcion para obtener el tipo de una idLocation.
    Valida si el idLocation ya fue declarada dentro del ambito.

    Parametros
    - nombre: nombre del idLocation
    - pilaVariable: pila de ambitos de las variables

    Retornos
    - <Error> si el idLocation no se encuentra en los ambitos
    - tipo en el caso de que se encuentre el idLocation
    '''
    for ambito in pilaVariable:
        if(nombre in ambito.keys()):
            return ambito[nombre].tipo

    return Error(f'La variable {nombre} no existe')


def getArrayLocationType(nombre, pilaVariable, expType):
    '''
    Funcion para obtener el tipo de una arrayLocation.
    Valida si el arrayLocation ya fue declarada dentro del ambito.

    Parametros
    - nombre: nombre del arrayLocation
    - pilaVariable: pila de ambitos de las variables

    Retornos
    - <Error> si el arrayLocation no se encuentra en los ambitos
    - tipo en el caso de que se encuentre el arrayLocation
    '''
    for ambito in pilaVariable:
        if(nombre in ambito.keys()):
            # existe el array
            if (ambito[nombre].arrayLong != None):
                # confirmamos que es array
                if (expType == 'int'):
                    # validamos que la exp sea int
                    return ambito[nombre].tipo
                else:
                    return Error(f"La <exp> del array '{nombre}' no es <int>")

    return Error(f"El array '{nombre}' no existe")
