class Descriptor:

    def __init__(self):
        '''
            Para cada registro disponible:

            Lleva la cuenta de los nombres de las
            variables cuyo valor actual se encuentra
            en ese registro

            {
                R1: [var1, var2]
            }

        '''
        self.registro = {}

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
        self.acceso = {}

    def actualizarCasoLD(self, R, x):
        '''
            Caso LD R, x
        '''
        self.registro[R] = [x]

        self.acceso[x].append(R)

    def actualizarCasoST(self, x, R):
        '''
            Caso ST x, R
        '''
        self.acceso[x].append(R)

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

    def getReg(self, instruccion):
        '''
        x = y + z

        Rx = None
        Ry = None
        Rz = None

        for variable in [y, z, x]:

            1. Evaluar si len(self.acceso[variable]) > 0
                1.1 ---

            4. Cuando no hay registro disponible

                Evaluar si x no es un operando
                    Borrar de forma temporal a x de todos los registros que lo contengan

                Si hay un registro vacío devolver ese registro

                Iterar sobre los registros que solo tengan un valor
                Identificar si esa variable esta en otro registro,
                de ser ese el caso seleccionar ese registro

                Evaluar que registro tiene menos variables para liberar
                    Pasar cada variable a su direccion de memoria y seleccionar ese registro


            Si es una asignacion solo seleccionar un registro





        '''

    def __repr__(self):
        return f""
