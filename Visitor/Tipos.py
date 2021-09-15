from Error import *
INT = 'int'
CHAR = 'char'
BOOLEAN = 'boolean'
STRUCT = 'struct'
VOID = 'void'
ERROR = 'error'


LITERAL = 'literal'
IDLOCATION = 'idLocation'
ASSIGNMENT = 'assignment'


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
