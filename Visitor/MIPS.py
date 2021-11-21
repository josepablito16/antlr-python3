from Descriptor import *


class MIPS:

    def __init__(self, datosFunciones):
        self.datosFuncion = datosFunciones
        self.registrosArg = ['$a0', '$a1', '$a2', '$a3']
        self.descriptor = Descriptor()
        print(self.datosFuncion)

    '''
        Etiquetas y saltos
    '''

    def construirGOTO(self, etiqueta):
        # hay varios tipos de jumps
        retorno = f"j {etiqueta}"
        pass

    def construirEtiqueta(self, etiqueta):
        print(f"{etiqueta}:")
        self.construirConfiguracionStack(etiqueta)

    def guardarParametrosEnStack(self, cantidadParametros):
        registrosParametros = ['$a0', '$a1', '$a2', '$a3']
        print("\t# Guardar en Stack los parametros de la funcion")
        for i in range(cantidadParametros):
            print(f"\tsw {registrosParametros.pop(0)}, {4 * i}($fp)")

    def construirRestauracionStack(self, etiqueta):
        ancho = self.datosFuncion[etiqueta].ancho
        if(ancho != 0):
            print(f'''
\t# Restauracion de stack
\tadd $sp, $fp, {ancho}
\tlw $fp, ($sp)
\tadd $sp, $sp, 4
\tlw $ra, ($sp)
\tadd $sp, $sp, 4
                ''')

    def construirConfiguracionStack(self, etiqueta):
        if (etiqueta == 'main'):
            ancho = self.datosFuncion[etiqueta].ancho
            if(ancho != 0):
                # Hay variables en main, preparar stack
                print(f'''
\t# Preparar stack
\tsw $fp, ($sp)
\tsub $fp, $sp, {ancho}
\tla $sp, ($fp)
                ''')
        elif (etiqueta != 'OutputInt'):
            # es cualquier funcion
            ancho = self.datosFuncion[etiqueta].ancho
            if(ancho != 0):
                # hay variables
                print(f'''
\t# Preparar stack
\tsub $sp, $sp, 4
\tsw, $ra, ($sp)
\tsub $sp, $sp, 4
\tsw $fp, ($sp)
\tsub $fp, $sp, {ancho}
\tla $sp, ($fp)
                ''')
                if(len(self.datosFuncion[etiqueta].argumentosTipos) > 0):
                    self.guardarParametrosEnStack(
                        len(self.datosFuncion[etiqueta].argumentosTipos))

    def construirIf(self, Rsrc, etiqueta):
        '''
            Bif. condicional si Rsrc es mayor que 0.
        '''
        retorno = f"bgtz {Rsrc}, {etiqueta}"
        pass

    '''
        Operaciones aritmeticas
    '''

    def construirMultiplicacion(self, Rdest, Rsrc1, Rsrc2):
        retorno = f"mul {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirSuma(self, cuadrupla):
        x = cuadrupla.resultado
        y = cuadrupla.arg1
        z = cuadrupla.arg2
        print("\t# Suma")

        self.descriptor.agregarAcceso(x)
        self.descriptor.agregarAcceso(y)
        self.descriptor.agregarAcceso(z)

        esLiteral = False
        literal = None
        try:
            y = int(y)
            esLiteral = True
            literal = y
        except:
            pass

        try:
            z = int(z)
            esLiteral = True
            literal = z
        except:
            pass

        registros = self.descriptor.getReg(x, y, z)
        if(esLiteral):
            print(
                f"\taddi {registros[0]}, {registros[1]}, {literal}")

        self.descriptor.eliminarAccesoTemporal(y)
        self.descriptor.eliminarAccesoTemporal(z)
        # print(self.descriptor.registro)
        # print(self.descriptor.acceso)
        # retorno = f"add {Rdest}, {Rsrc1}, {Rsrc2}"

    def construirDivision(self, Rdest, Rsrc1, Rsrc2):
        retorno = f"div {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirMenos(self, Rdest, Rsrc1):
        retorno = f"neg {Rdest}, {Rsrc1}"
        pass

    def construirResta(self, Rdest, Rsrc1, Rsrc2):
        retorno = f"sub {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    '''
        Operaciones logicas
    '''

    def construirNegacion(self, Rdest, Rsrc1):
        retorno = f"not {Rdest}, {Rsrc1}"
        pass

    def construirAnd(self, Rdest, Rsrc1, Rsrc2):
        retorno = f"and {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirOr(self, Rdest, Rsrc1, Rsrc2):
        retorno = f"or {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    '''
        Operacion de comparacion
    '''

    def construirComparacionIgual(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest a 1 si Rsrc1 y Rsrc2 son iguales, en otro caso pone 0
        '''
        retorno = f"seq {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirComparacionMayorIgual(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest a 1 si Rsrc1 es mayor o igual a Rsrc2,
            y 0 en otro caso (para números con signo).
        '''
        retorno = f"sge {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirComparacionMayor(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest a 1 si Rsrc1 es mayor a Rsrc2,
            y 0 en otro caso (para números con signo).
        '''
        retorno = f"sgt {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirComparacionMenorIgual(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest a 1 si Rsrc1 es menor o igual a Rsrc2,
            y 0 en otro caso (para números con signo).
        '''
        retorno = f"sle {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirComparacionMenor(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest a 1 si Rsrc1 es menor a Rsrc2,
            y 0 en otro caso (para números con signo).
        '''
        retorno = f"slt {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    def construirComparacionNoIgual(self, Rdest, Rsrc1, Rsrc2):
        '''
            Pone Rdest to 1 si el registro Rsrc1 no es igual a Rsrc2
            y 0 en otro caso
        '''
        retorno = f"sne {Rdest}, {Rsrc1}, {Rsrc2}"
        pass

    '''
        Cargas
    '''

    def construirCarga(self, cuadrupla):
        '''
            EJ: Rdest = Rsrc1
        '''
        print('\t# Igualar')
        x = cuadrupla.resultado
        y = cuadrupla.arg1
        # TODO manejar caso R, correr el programa
        if ((y == 'R') and (x.find('fp') != -1)):
            offset = x[x.find('[') + 1:x.find(']')]
            print(f"\tsw $v0, {offset}($fp)")
        elif (x.find('fp') != -1):
            registros = self.descriptor.getReg(x, y)
            offset = x[x.find('[') + 1:x.find(']')]
            print(f"\tsw {registros[0]}, {offset}($fp)")
        #retorno = f"move {Rdest}, {Rsrc}"

    '''
        Almacenamiento
    '''

    def construirAlmacenamiento(self, Rsrc, direccion):

        retorno = f"sw {Rsrc}, {direccion}"
        pass

    '''
        Funciones
    '''

    def construirLlamarFuncion(self, nombre):
        print(f"\tjal {nombre}")

    def construirRetorno(self, reg, etiqueta):
        print("\n\t# Se carga valor de retorno")
        try:
            literal = int(reg)
            print(f'\tli $v0, {literal}')
        except:
            # TODO cargar valor de retorno cuando no es una literal
            retorno = f"move $v0, {reg}"
            pass

        self.construirRestauracionStack(etiqueta)
        print("\tjr $ra")
        self.restablecerRegistroParametros()

    def construirParametro(self, parametro):
        if (parametro.find('fp') != -1):
            offset = parametro[parametro.find('[') + 1:parametro.find(']')]
            print(f"""
\t# Cargar parametros
\tlw {self.registrosArg.pop(0)}, {offset}($fp)""")
        elif(parametro == 'R'):
            print(f"""
\t# Cargar parametros
\tmove {self.registrosArg.pop(0)}, $v0""")

    def construirRetornoSimple(self):
        '''
            Transfiere el control de nuevo a la llamada de funcion
        '''
        print('\tjr $ra')
        self.restablecerRegistroParametros()

    def constuirInputInt(self):
        print('''
\t# Se imprime mensaje al usuario
\tli $v0, 4
\tla $a0, mensajeInput
\tsyscall

\t# Se lee el input del usuario
\tli $v0,5
\tsyscall
\tjr $ra
        ''')

    def constuirOutputInt(self):
        print('''
\t# Se imprime numero en pantalla
\tli $v0, 1
\tsyscall

\t# Se hace un salto de linea
\tli $v0, 4
\tla $a0, saltoLinea
\tsyscall
\tjr $ra
        ''')

    '''
        Complementarias
    '''

    def guardarEstadoMaquina(self):
        print("\t# guardar estado de maquina")
        for i in self.descriptor.acceso:
            if(i.find('fp') != -1):
                offset = i[i.find('[') + 1:i.find(']')]
                print(
                    f"sw {self.descriptor.buscarRegistroEnAcceso(i)}, {offset}($fp)")
        self.descriptor.limpiarDescriptores()

    def restablecerRegistroParametros(self):
        self.registrosArg = ['$a0', '$a1', '$a2', '$a3']

    def encabezado(self, espacioGlobal):
        newLine = "\n"
        print(f'''
.data
.align 2
    G_: .space {espacioGlobal}
    mensajeInput: .asciiz "Ingrese un número entero: "
    saltoLinea: .asciiz "{repr(newLine).replace("'","")}"
.text
        ''')

    def finPrograma(self):
        print('''
\t# fin del programa
\tli $v0, 10
\tsyscall
        ''')

    def generarCodigo(self, cuadruplas):
        funcionActual = ""
        for linea in cuadruplas:
            if linea.op == 'FUNCTION':
                self.construirEtiqueta(linea.arg1)
                funcionActual = linea.arg1
                if(linea.arg1 == 'InputInt'):
                    self.constuirInputInt()
                elif(linea.arg1 == 'OutputInt'):
                    self.constuirOutputInt()
                continue
            elif linea.op == 'RETURN':
                if (funcionActual == 'InputInt'):
                    self.construirRetornoSimple()
                else:
                    self.construirRetorno(linea.arg1, funcionActual)
                continue

            elif linea.op == 'END FUNCTION':
                funcionActual = ""
                self.descriptor.limpiarDescriptores()
                continue
            elif linea.op == 'CALL':
                self.guardarEstadoMaquina()
                self.construirLlamarFuncion(linea.arg1)
                continue
            elif linea.op == 'PARAM':
                self.construirParametro(linea.arg1)
                continue
            elif linea.op == '+':
                self.construirSuma(linea)
                continue
            elif linea.op == '=':
                # print(self.descriptor.registro)
                # print(self.descriptor.acceso)
                # linea.debug()
                self.construirCarga(linea)
                continue

            else:
                pass
                # linea.debug()
            linea.debug()

    def __repr__(self):
        return f""
