import copy
import json
from typing import ItemsView


class Descriptor:

    def __init__(self):
        self.registro = {
            '$t1': [],
            '$t2': [],
            '$t3': [],
            '$t4': [],
            '$t5': [],
            '$t6': [],
            '$t7': [],
            '$t8': [],
            '$t9': [],
        }
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

    def agregarAcceso(self, variable):
        if(variable == 'R'):
            return
        try:
            variable = int(variable)
            return
        except:
            if variable not in self.acceso.keys():
                if (variable.find('fp') != -1):
                    self.acceso[variable] = [variable]
                elif (variable.find('G') != -1):
                    self.acceso[variable] = [variable]
                else:
                    self.acceso[variable] = []

    def eliminarAccesoTemporal(self, temporal):
        try:
            temporal = int(temporal)
            return
        except:
            pass

        if (temporal.find('t') == -1):
            return

        for i in self.acceso[temporal]:
            try:
                self.registro[i].remove(temporal)
            except:
                continue
        del self.acceso[temporal]

    def limpiarDescriptores(self):
        for key in self.registro.keys():
            self.registro[key] = []
        self.acceso = {}

    def actualizarCasoLD(self, R, x):
        '''
            Caso LD R, x
        '''
        if(x.find('t') == -1):
            if (x.find('fp') != -1):
                offset = x[x.find('[') + 1:x.find(']')]
                print(f'\tlw {R}, {offset}($fp)')

        self.registro[R] = [x]

        self.acceso[x].append(R)

    def eliminarVariableDeRegistro(self, variable):
        '''
            Se elimina variable de todos los
            registros

            Parametro:
            - variable: variable a eliminar

        '''
        for key, value in self.registro.items():
            try:
                value.remove(variable)
            except:
                continue

    def actualizarCasoST(self, x, R):
        '''
            Caso ST x, R
        '''
        print(f'ST {x}, {R}')
        self.eliminarVariableDeRegistro(x)
        self.acceso[x] = [x]  # solo sería ella misma

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
            if (i.find('$t') != -1):
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

    def iterarRegistrosCasiLibres(self, registro, usados):
        '''
            Itera sobre los registros que solo
            tienen un valor, si esa variable
            esta en otro registro, retorna R.

            Parametros:
            - registro: registroTemp para iterar
            - usados: parametros usados si no se
            quieren repetir

            Retorno:
            - R si hay un registro que cumpla,
            de lo contrario nada.
        '''
        for key, value in registro.items():
            if len(value) == 1:
                registros = self.getCantRegistrosEnAcceso(value[0])

                if (len(registros) > 2):
                    registros.remove(key)
                    if registros[0] in usados:
                        continue
                    return registros[0]

    def getMejorRegistro(self, registro, usados):
        '''
            Funcion para evaluar que registro tiene
            menos variables para liberar.

            Parametros:
            - registro: registro temporal
            - usados: registros usados por
            si no se quieren repetir

            Retorno:
            - Registro con menos variables.
        '''
        registroSort = sorted(
            registro.items(), key=lambda x: len(x[1]), reverse=False)

        for i in registroSort:
            if i[0] not in usados:
                return i[0]

    def getRegAuxiliar(self, variable, x=None, usados=[]):
        '''
            Funcion auxiliar para obtener un registro

            Parametros:
            - variable: variable a obtener un registro.
            - x: si se pasa como parametro, significa
            que x es un operando.
            - usados: registros usados, si en dado caso
            no se quieren repetir.

            Retorno:
            - Registro disponible para variable.
        '''
        if (len(self.acceso[variable]) > 0):
            # evaluar si en acceso[variable]
            # hay algun registro, si lo hay
            # lo llamaremos R
            Rtemp = self.buscarRegistroEnAcceso(variable)
            if (Rtemp):
                #print(f'{variable} -> Caso 1')
                return Rtemp

        # Si hay algun registro libre, retornarlo
        Rtemp = self.getRegistroVacio()
        if(Rtemp):
            #print(f'{variable} -> Caso 2')
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
            if not Rtemp in usados:
                #print(f'{variable} -> Caso 3')
                self.actualizarCasoLD(Rtemp, variable)
                return Rtemp

        # Iterar sobre los registros que solo tengan
        # un valor, identificar si esa variable esta
        # en otro registro, de ser ese el caso seleccionar
        # ese registro (R)
        Rtemp = self.iterarRegistrosCasiLibres(registroTemp, usados)
        if Rtemp:
            #print(f'{variable} -> Caso 4')
            self.actualizarCasoLD(Rtemp, variable)
            return Rtemp

        # Evaluar que registro tiene menos variables para liberar
        # Pasar cada variable a su direccion de memoria y
        # seleccionar ese registro (R)
        #print(f'{variable} -> Caso 5')
        Rtemp = self.getMejorRegistro(registroTemp, usados)
        self.actualizarMultipleST(Rtemp)
        self.actualizarCasoLD(Rtemp, variable)
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

            registro = self.getRegAuxiliar(y, xOperando, registros)
            registros.append(registro)
            registros.append(registro)

        else:
            # es una operacion de la
            # forma x = y + z

            if (x == y or x == z):
                xOperando = x

            for variable in [x, y, z]:
                if(variable == 'R'):
                    continue
                try:
                    variable = int(variable)
                    continue
                except:
                    registros.append(self.getRegAuxiliar(
                        variable, xOperando, registros))

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
        'R1': ['t1'],
        'R2': ['t1', 'fp[0]'],
        'R3': []
    }

    d.acceso = {
        't1': ['R1', 'R2'],
        'fp[0]': ['R2'],
    }

    d.eliminarAccesoTemporal('fp[0]')
    # d.eliminarAccesoTemporal('t1')
    print(d.registro)
    print(d.acceso)
