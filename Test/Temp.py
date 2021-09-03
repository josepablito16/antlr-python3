lista = ['B', 'c', 'd']

contador = 0

while (contador < len(lista) - 1):
    print(f'{lista[contador]} - {lista[contador + 1]}')
    print()
    lista.pop(1)
    lista.insert(1, 'int')
    contador += 1
