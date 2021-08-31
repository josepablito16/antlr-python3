def procesar(expresion):
    i = 0
    print(f'''
        expresion
        {expresion}
        ''')
    while (i < len(expresion)):
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
    print(f'resultado: {expresion}\n')


test = [
    # - 1 + 5 * 6
    ['minus', 'int', 'intOp', 'int', 'intOp', 'int'],

    # 7 - 3 * 2
    ['int', 'intOp', 'int', 'intOp', 'int'],

    # 8 >= 1
    ['int', 'relOp', 'int'],

    # true < false
    ['boolean', 'relOp', 'boolean'],

    # true == false
    ['boolean', 'eqOp', 'boolean'],

    # 'a' != 'b'
    ['char', 'eqOp', 'char'],

    # true != 'b'
    ['boolean', 'eqOp', 'char'],

    # true && false
    ['boolean', 'boolOp', 'boolean'],

    # 1 || false
    ['int', 'boolOp', 'boolean']



]

'''
CASOS A REVISAR
-1 + ('a' + true)
'''

for j in test:
    procesar(j)
