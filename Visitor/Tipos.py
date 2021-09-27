from Nodo import Nodo
from Error import *
INT = 'int'
CHAR = 'char'
BOOLEAN = 'boolean'
STRUCT = 'struct'
VOID = 'void'
ERROR = 'error'


LITERAL = 'literal'
IDLOCATION = 'idLocation'
IDLOCATIONDOT = 'idLocationDot'
ASSIGNMENT = 'assignment'
ARRAYLOCATION = 'arrayLocation'
ARRAYLOCATIONDOT = 'arrayLocationDot'
OPERACION = 'operacion'
METHOD = 'method'


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

    return Error(f"La variable '{nombre}' no existe")


def getArrayLocationType(nombre, pilaVariable):
    '''
    Funcion para obtener el tipo de una arrayLocation.
    Valida si el arrayLocation ya fue declarada dentro del ambito
    y si es un array.

    Parametros
    - nombre: nombre del arrayLocation
    - pilaVariable: pila de ambitos de las variables

    Retornos
    - <Error> si el arrayLocation no se encuentra en los ambitos
    - tipo en el caso de que se encuentre el arrayLocation
    '''
    for ambito in pilaVariable:
        if(nombre in ambito.keys()):
            # si existe la variable
            if(ambito[nombre].arrayLong != None):
                # si es array
                return ambito[nombre].tipo
            else:
                return Error(f"La variable '{nombre}' no es un array")

    return Error(f"El array '{nombre}' no existe")


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

    return Error(f"La funcion '{nombre}' no existe")


def validarTiposArgumentos(nombre, tiposArgumentos, pilaFuncion):
    '''
    Funcion para validar si los tipos de una llamada de funcion son equivalentes
    a los tipos de la declaracion de la funcion

    Parametros:
    - nombre: nombre de la funcion a evaluar
    - tiposArgumentos: lista de <Nodo> con la informacion de los argumentos en la llamada de la funcion
    - pilaFuncion: pila con las funciones declaradas

    Retorno:
    - <Error> si en dado caso la cantidad o tipo de argumentos no coinciden
    '''
    for ambito in pilaFuncion:
        if(nombre in ambito.keys()):

            if len(tiposArgumentos) != len(ambito[nombre].argumentosTipos):
                return Error("La cantidad de los argumentos no coinciden con la definicion")

            for arg in ambito[nombre].argumentosTipos:
                if not(arg == tiposArgumentos.pop(0).tipo):
                    return Error("Los tipos de los argumentos no coinciden con la definicion")


def validarTiposAsignacion(derecho, izquierdo):
    '''
    Funcion que valida si el tipo del lado derecho de una
    asignacion es el mismo que del lado izquierdo

    Parametros:
    - derecho: Objeto <Nodo> con la informacion del lado derecho de la asignacion
    - izquierdo: Objeto <Nodo> con la informacion del lado izquierdo de la asignacion

    Return:
    - Si los tipos coinciden retornamos el tipo
    - Caso contrario retornamo un objeto <Error>
    '''
    if (derecho.tipo == izquierdo.tipo != ERROR):
        return derecho.tipo
    else:
        return Error(f"expresion de tipo '{derecho.tipo}' no se puede asignar a variable de tipo '{izquierdo.tipo}'")


def validarTiposOperacion(nodos):
    '''
    Funcion para validar una lista de nodos que se estan operando

    Parametros:
    - nodos: lista de tipo <Nodo>

    Return:
    - si todos los tipos son iguales, retornamos el tipo
    - caso contrario Error
    '''
    if not isinstance(nodos, list):
        return nodos.tipo

    control = nodos[0].tipo

    for i in nodos:
        if (control != i.tipo):
            return Error('Se esta intentando operar distintos tipos de datos')

    return control


def validarEstructura(nombre, pilaVariable):
    '''
    Funcion que valida si una variable es una estructura decalarada.

    Parametros:
    - nombre: nombre de la variable a evaluar
    - pilaVariable: pila con la informacion de todos los ambitos

    Retorno:
    - tipo de estructura
    - <Error> en dado caso no exista una variable con ese nombre, o no sea de tipo
    estructura
    '''
    for ambito in pilaVariable:
        if(nombre in ambito.keys()):
            if (not ambito[nombre].isEstructura):
                return Error(f"La variable '{nombre}' no es una estructura")
            else:
                return ambito[nombre].tipo

    return Error(f"La variable '{nombre}' no existe")


def validarEstructuraArray(nombre, pilaVariable):
    '''
    Funcion que valida si una variable es una estructura decalarada y tambien
    que sea un array

    Parametros:
    - nombre: nombre de la variable a evaluar
    - pilaVariable: pila con la informacion de todos los ambitos

    Retorno:
    - tipo de estructura
    - <Error> en dado caso no exista una variable con ese nombre, o no sea de tipo
    estructura
    '''
    for ambito in pilaVariable:
        if(nombre in ambito.keys()):
            if (ambito[nombre].arrayLong == None):
                return Error(f"La variable '{nombre}' no es un array")

            if (not ambito[nombre].isEstructura):
                return Error(f"La variable '{nombre}' no es una estructura")
            else:
                return ambito[nombre].tipo

    return Error(f"La variable '{nombre}' no existe")
