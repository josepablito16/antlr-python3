import copy
import json
from typing import ItemsView


class Descriptor:

    def __init__(self):
        self.registro = {}
        '''
            Para cada registro disponible:

            Lleva la cuenta de los nombres de las
            variables cuyo valor actual se encuentra
            en ese registro

            {
                R1: [var1, var2]
            }

        '''

        self.acceso = {}
        '''
            Para cada variable del programa:

            Lleva la cuenta de la ubicacion o
            ubicaciones en las que puede
            encontrarse el valor actual de
            esa variable.

            La ubicacion podría ser:
                registro
                direccion de memoria
                ubicacion en la pila

            {
                t1: [R1,...]
                fp[0]: [R1,...]
                G[0]: [R1,...]
            }
        '''

    def actualizarCasoLD(self, R, x):
        '''
            Caso LD R, x
        '''
        print(f'LD {R}, {x}')
        self.registro[R] = [x]

        self.acceso[x].append(R)

    def actualizarCasoST(self, x, R):
        '''
            Caso ST x, R
        '''
        print(f'ST {x}, {R}')
        self.acceso[x].append(R)

    def actualizarMultipleST(self, R):
        for var in self.registro[R]:
            self.actualizarCasoST(var, R)

    def actualizarCasoOP(self, Rx, x):
        '''
            Caso ADD Rx, Ry, Rz
            x = y + z
        '''
        self.registro[Rx] = [x]
        self.acceso[x] = [Rx]

        for i in self.acceso.keys():
            if (i == x):
                continue
            try:
                self.acceso[i].remove(Rx)
            except:
                pass

    def actualizarCasoCopia(self, x, Ry):
        '''
            Caso x = y
        '''
        self.registro[Ry].append(x)
        self.registro[x] = [Ry]
        pass

    def buscarRegistroEnAcceso(self, variable):
        '''
            Funcion para buscar un registro en
            el acceso de una variable

            Parametros:
            - variable: variable a evaluar

            Return:
            - Registro o Nada si no hay un registro
        '''
        for i in self.acceso[variable]:
            if (i.find('R') != -1):
                return i

    def getRegistroVacio(self, registro=None):
        '''
            Funcion para obtener un registro libre

            Retorno:
            - R si hay registro libre, de lo contrario
            nada.
        '''
        if (not registro):
            registro = copy.deepcopy(self.registro)

        for key, value in registro.items():
            if (len(value) == 0):
                return key

    def eliminarXTemp(self, variable):
        '''
            Crea un registro sin variable

            Parametro:
            - variable: variable a eliminar

            Retorno:
            - registro sin variable
        '''
        registroTemp = {}
        for key, value in copy.deepcopy(self.registro.items()):
            try:
                registroTemp[key] = value.remove(variable)
            except:
                continue
        return registroTemp

    def getCantRegistrosEnAcceso(self, variable):
        '''
            Retorna la lista de registros en los
            que esta una variable

            Parametros:
            - variable: variable a evaluar

            Retorno:
            - <list> registros
        '''
        registros = []
        for i in self.acceso[variable]:
            if (i.find('R') != -1):
                registros.append(i)
        return registros

    def iterarRegistrosCasiLibres(self, registro):
        '''
            Itera sobre los registros que solo
            tienen un valor, si esa variable
            esta en otro registro, retorna R.

            Parametros:
            - registro: registroTemp para iterar

            Retorno:
            - R si hay un registro que cumpla,
            de lo contrario nada.
        '''
        for key, value in registro.items():
            if len(value) == 1:
                registros = self.getCantRegistrosEnAcceso(value[0])

                if (len(registros) > 2):
                    registros.remove(key)
                    return registros[0]

    def getMejorRegistro(self, registro):
        '''
            Funcion para evaluar que registro tiene
            menos variables para liberar.

            Parametros:
            - registro: registro temporal

            Retorno:
            - Registro con menos variables.
        '''
        registroSort = sorted(
            registro.items(), key=lambda x: len(x[1]), reverse=False)

        return registroSort[0][0]

    def getRegAuxiliar(self, variable, x=None):
        '''
            Funcion auxiliar para obtener un registro

            Parametros:
            - variable: variable a obtener un registro.
            - x: si se pasa como parametro, significa
            que x es un operando.

            Retorno:
            - Registro disponible para variable.
        '''
        if (len(self.acceso[variable]) > 0):
            # evaluar si en acceso[variable]
            # hay algun registro, si lo hay
            # lo llamaremos R
            Rtemp = self.buscarRegistroEnAcceso(variable)
            if (Rtemp):
                print(f'{variable} -> Caso 1')
                return Rtemp

        # Si hay algun registro libre, retornarlo
        Rtemp = self.getRegistroVacio()
        if(Rtemp):
            print(f'{variable} -> Caso 2')
            self.actualizarCasoLD(Rtemp, variable)
            return Rtemp

        # cuando no hay registro disponible:

        registroTemp = None

        # Evaluar si x no es un operando
        if (x):
            # eliminar de forma temporal a x de los
            # registros que lo contengan
            registroTemp = self.eliminarXTemp(x)
        else:
            registroTemp = copy.deepcopy(self.registro)

        # Si hay algun registro libre, retornarlo
        Rtemp = self.getRegistroVacio(registroTemp)
        if(Rtemp):
            print(f'{variable} -> Caso 3')
            self.actualizarCasoLD(Rtemp, variable)
            return Rtemp

        # Iterar sobre los registros que solo tengan
        # un valor, identificar si esa variable esta
        # en otro registro, de ser ese el caso seleccionar
        # ese registro (R)
        Rtemp = self.iterarRegistrosCasiLibres(registroTemp)
        if Rtemp:
            print(f'{variable} -> Caso 4')
            self.actualizarCasoLD(Rtemp, variable)
            return Rtemp

        # Evaluar que registro tiene menos variables para liberar
        # Pasar cada variable a su direccion de memoria y
        # seleccionar ese registro (R)
        Rtemp = self.getMejorRegistro(registroTemp)
        self.actualizarMultipleST(Rtemp)
        self.actualizarCasoLD(Rtemp, variable)
        print(f'{variable} -> Caso 5')
        return Rtemp

    def getReg(self, x, y, z=None):
        '''
            Funcion principal para obtener
            los registros dado x, y, z.

            x = y + z
            x = y

            Parametros:
            - x,y,z: variables de una instruccion

            Retorno:
            - lista de registros de la forma [Rx, Ry, Rz]
        '''
        registros = []
        xOperando = None

        if (z == None):
            # sabemos que es asignacion
            # asi que solo necesitamos
            # 1 registro
            if (x == y):
                xOperando = x

            registro = self.getRegAuxiliar(y, xOperando)
            registros.append(registro)
            registros.append(registro)

        else:
            # es una operacion de la
            # forma x = y + z

            if (x == y or x == z):
                xOperando = x

            for variable in [x, y, z]:
                registros.append(self.getRegAuxiliar(variable, xOperando))

        return registros

    def debug(self):
        print('##################')
        print('Registro:')
        for key, item in self.registro.items():
            print(f'{key}: {item}')

        print('\nAcceso:')
        for key, item in self.acceso.items():
            print(f'{key}: {item}')
        print('##################')

    def __repr__(self):
        return f""


if __name__ == '__main__':
    d = Descriptor()
    d.registro = {
        'R1': [],
        'R2': [],
        'R3': []
    }

    d.acceso = {
        'a': ['a'],
        'b': ['b'],
        'c': ['c'],
        'd': ['d'],
        't': [],
        'u': [],
        'v': [],
    }

    # t = a - b
    d.debug()
    print('t = a - b')
    print(d.getReg(x='t', y='a', z='b'))
    print()

    # u = a - c
    d.debug()
    print('u = a - c')
    print(d.getReg(x='u', y='a', z='c'))
    print()

    # v = t + u
    # a = d
    # d = v + u
