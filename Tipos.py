
def procesarExp(expresion):
    '''
    Funcion para validar los tipos de una expresion.

    Parametros
    - expresion: lista de tipos de datos Ej: ['int']
    '''
    i = 0
    print('###########################')
    while (i < len(expresion)):
        print(f'''
            procesarExp {i}
            {expresion}
            ''')
        # regla not
        if(expresion[i] == 'not'):
            # si el siguiente es boolean, entonces el resultado es boolean
            if (expresion[i+1] == 'boolean'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'boolean')
            else:
                # sino el resultado es err
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            continue

        # regla minus
        if(expresion[i] == 'minus'):
            # si el siguiente es int, entonces el resultado es int
            if (expresion[i+1] == 'int'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'int')
            else:
                # sino el resultado es err
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            continue

        # regla intOp
        if (expresion[i] == 'intOp'):
            if(expresion[i-1] == expresion[i+1] == 'int'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'int')
            else:
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            i -= 1
            continue

        # regla mayor, menor
        if (expresion[i] == 'relOp'):
            if(expresion[i-1] == expresion[i+1] == 'int'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'boolean')
            else:
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            i -= 1
            continue

        # regla ==, !=
        if (expresion[i] == 'eqOp'):
            if(expresion[i-1] == expresion[i+1] != 'err'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'boolean')
            else:
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            i -= 1
            continue

        # regla &&, ||
        if (expresion[i] == 'boolOp'):
            if(expresion[i-1] == expresion[i+1] == 'boolean'):
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'boolean')
            else:
                expresion.pop(0)
                expresion.pop(0)
                expresion.pop(0)
                expresion.insert(0, 'err')
            i -= 1
            continue

        # print(expresion[i])
        i += 1

    print('###########################')
    return expresion.pop()
