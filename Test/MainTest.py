from Funcion import *
from Variable import *


f1 = Funcion("void", [], Variable('r1', 'int'))
assert f1.err == 'Funcion void no retorna nada', "Funcion void no retorna nada"


f2 = Funcion("int", [])
assert f2.err == 'Falta retorno de funcion', "Falta retorno de funcion"


f3 = Funcion("int", [], Variable('r1', 'float'))
assert f3.err == 'El tipo de la funcion y el tipo de retorno no coinciden', "El tipo de la funcion y el tipo de retorno no coinciden"

f4 = Funcion("int", [], Variable('r1', 'int'))
assert f4.err == None, "Funcion bien declarada"
