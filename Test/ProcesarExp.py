

def procesar(exp):
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
    operadores = ['intOp', 'relOp', 'eqOp', 'boolOp']
    pila = []
    for i in exp:
        if i not in operadores:
            # no es operador
            pila.append(i)
        else:
            # es operador

            # TODO relga not
            # TODO relga minus

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

    print(pila)


test = [
    ['intOp', 'intOp', 'int', 'int', 'intOp', 'int', 'int'],
    ['relOp', 'intOp', 'int', 'int', 'intOp', 'int', 'int'],
    ['intOp', 'int', 'intOp', 'int', 'int'],
    ['boolOp', 'boolean', 'boolean'],
    ['boolOp', 'boolean', 'int']
]


for j in test:
    procesar(j)
