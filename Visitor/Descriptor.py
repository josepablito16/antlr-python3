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
        pass

    def __repr__(self):
        return f""
