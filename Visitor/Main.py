from typing import List
from antlr4 import *
from Cuadrupla import Cuadrupla
from decafLexer import decafLexer
from decafVisitor import decafVisitor
from decafParser import decafParser

from Estructura import *
from Variable import *
from Funcion import *
from Error import *


from Nodo import Nodo
import Tipos as tipos

import copy

# pilas donde se manejan los ambitos
pilaVariable = []
pilaFuncion = []
pilaEstructura = []

# ancho de cada tipo de dato
ancho = {'int': 4,
         'char': 2,
         'boolean': 1
         }

# offsets de variables
offsetGlobal = 0
offsetLocal = []

offsetLocationDot = 0
procesandoLocation = False
isLocationLocal = True
codigoLocation = []
ultimaDireccionLocation = None

# contador de temporales
contadorTemporales = 0

# contadores de etiquetas
contadorEtiquetasTrue = 0
contadorEtiquetasFalse = 0
contadorEtiquetasEndIf = 0
contadorEtiquetasStartWhile = 0
contadorEtiquetasEndWhile = 0

FAIL = '\033[91m'
ENDC = '\033[0m'

nombreFuncionTemp = ""


class EvalVisitor(decafVisitor):

    def nuevaEtiqueta(self, tipoEtiqueta):
        '''
            Metodo que genera una etiqueta nueva.

            Parametros:
            - tipoEtiqueta: tipo de etiqueta, puede ser:
                true, false, endIf, startWhile, endWhile

            Retorno:
            - nombre de la etiqueta
        '''
        global contadorEtiquetasTrue
        global contadorEtiquetasFalse
        global contadorEtiquetasEndIf
        global contadorEtiquetasStartWhile
        global contadorEtiquetasEndWhile

        if (tipoEtiqueta == 'true'):
            retorno = f'LABEL_TRUE_{contadorEtiquetasTrue}'
            contadorEtiquetasTrue += 1
            return retorno

        if (tipoEtiqueta == 'false'):
            retorno = f'LABEL_FALSE_{contadorEtiquetasFalse}'
            contadorEtiquetasFalse += 1
            return retorno

        if (tipoEtiqueta == 'endIf'):
            retorno = f'LABEL_ENDIF_{contadorEtiquetasEndIf}'
            contadorEtiquetasEndIf += 1
            return retorno

        if (tipoEtiqueta == 'startWhile'):
            retorno = f'LABEL_STARTWHILE_{contadorEtiquetasStartWhile}'
            contadorEtiquetasStartWhile += 1
            return retorno

        if (tipoEtiqueta == 'endWhile'):
            retorno = f'LABEL_ENDTWHILE_{contadorEtiquetasEndWhile}'
            contadorEtiquetasEndWhile += 1
            return retorno

    def calcularOffset(self, tipo, num=1):
        '''
            Funcion para calcular el offset de una
            variable segun el tipo.

            Parametros:
            - tipo: tipo de variable
            - num: cantidad de elementos (se usa para arreglos)

            Retorno:
            - <int>, <bool> : offset, si es local o no
        '''
        global offsetLocal
        global offsetGlobal
        isLocal = None
        offset = None
        try:  # TODO calcular ancho para estructuras y arrays
            if (len(pilaVariable) > 1):
                # si el largo del array de pilaVariable es mayor a 1 es offsetLocal
                isLocal = True
                offset = offsetLocal[-1]
                offsetLocal[-1] += ancho[tipo] * num
            else:
                # sino es offsetGlobal
                isLocal = False
                offset = offsetGlobal
                offsetGlobal += ancho[tipo] * num
        except:
            pass

        return offset, isLocal

    def getIsLocal(self):
        '''
            Funcion para retorna si uan funcion es local o no

            Retorno:
            - <bool> : si es local o no
        '''
        isLocal = None
        try:
            if (len(pilaVariable) > 1):
                # si el largo del array de pilaVariable es mayor a 1 es offsetLocal
                isLocal = True
            else:
                # sino es offsetGlobal
                isLocal = False
        except:
            pass

        return isLocal

    def generarTemporal(self, nombre):
        """
            Funcion para calcular la temporal dada un
            nombre de variable

            Parametros:
            - nombre: nombre de la variable

            Retorno:
            - <str> fp para variables locales, G para variables globales
            con su offset
        """
        # TODO manejar, estructuras
        for i in range(len(pilaVariable) - 1, -1, -1):
            ambito = pilaVariable[i]
            if(nombre in ambito.keys()):

                offset = ambito[nombre].offset

                if (ambito[nombre].isLocal):
                    return f"fp[{offset}]"
                else:
                    return f"G[{offset}]"

    def getOffset(self, nombre):
        """
            Funcion para obtener el offset de una variable

            Parametros:
            - nombre: nombre de la variable

            Retorno:
            - <int> offset de la variable
        """
        for i in range(len(pilaVariable) - 1, -1, -1):
            ambito = pilaVariable[i]
            if(nombre in ambito.keys()):
                return ambito[nombre].offset

    def generarTemporalArray(self, nombre, temporal):
        """
            Funcion para calcular la temporal dada un
            nombre de una variable tipo array

            Parametros:
            - nombre: nombre de la variable
            - temporal: nombre de la temporal

            Retorno:
            - <str> fp para variables locales, G para variables globales
            siendo su offset una temporal
        """
        # TODO manejar, estructuras
        for i in range(len(pilaVariable) - 1, -1, -1):
            ambito = pilaVariable[i]
            if(nombre in ambito.keys()):

                if (ambito[nombre].isLocal):
                    return f"fp[{temporal}]"
                else:
                    return f"G[{temporal}]"

    def nuevaTemporal(self):
        global contadorTemporales
        temporal = f"t{contadorTemporales}"
        contadorTemporales += 1
        return temporal

    def agregarVariableATabla(self, nombre, variable):
        '''
        Funcion que valida si una variable ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Parametros
        - nombre: string con el nombre de la variable
        - variable: objeto Variable con la informacion de la variable a ingresar.
        '''

        if(nombre in pilaVariable[-1].keys()):
            return Error('Esta variable ya existe')
        else:
            pilaVariable[-1][nombre] = variable

        print(f'''
                # Pila Variables
                {pilaVariable}
                ''')

    def agregarStructATabla(self, nombre, estructura):
        '''
        Funcion que valida si una estructura ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Parametros
        - nombre: string con el nombre de la estructura
        - estructura: objeto estructura con la informacion de la estructura a ingresar.
        '''
        """
        print(f'''
        agregarStructATabla
        nombre = {nombre}
        pila = {pilaEstructura}
        ''')
        """
        if(nombre in pilaEstructura[-1].keys()):
            return Error(f"La estructura '{nombre}' ya ha sido declarada antes.")
        else:
            pilaEstructura[-1][nombre] = estructura

        """
        print(f'''
                # Pila Estructura
                {pilaEstructura}
                ''')
        """

    def agregarFuncionATabla(self, nombre, funcion):
        '''
        Funcion que valida si una funcion ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Solo se agrega a la tabla si no tiene errores en los argumentos

        Parametros
        - nombre: string con el nombre de la funcion
        - funcion: objeto Funcion con la informacion de la funcion a ingresar.
        '''
        # si no tiene error en los  argumentos se agrega a talba
        if not(isinstance(funcion.argumentosTipos, str)):
            if(nombre in pilaFuncion[-1].keys()):
                return Error('Esta funcion ya existe')
            else:
                pilaFuncion[-1][nombre] = copy.deepcopy(funcion)

            """
            print(f'''
                    # Pila funciones
                    {pilaFuncion}
                    ''')
            """

    def validarEstructura(self, nombreEstructura):
        '''
        Funcion que valida si una estructura ya existe en la tabla actual
        si no existe retorna error, caso contrario True.

        Parametros
        - nombreEstructura: string con el nombre de la estructura
        '''
        if(nombreEstructura in pilaEstructura[-1].keys()):
            return True
        else:
            return Error(f"La estructura '{nombreEstructura}' no ha sido definida.")

    def agregarAmbito(self, variable=True, estructura=False, funcion=False):
        '''
        Funcion para agregar un ambito

        Parametros:
        - variable: bool para indicar si se desea agregar un ambito de variables.
        - estructura: bool para indicar si se desea agregar un ambito de estructuras.
        - funcion: bool para indicar si se desea agregar un ambito de funciones.
        '''
        if variable:
            offsetLocal.append(0)
            pilaVariable.append({})
        if estructura:
            pilaEstructura.append({})
        if funcion:
            pilaFuncion.append({})

    def quitarAmbito(self, variable=True, estructura=False, funcion=False):
        '''
        Funcion para quitar un ambito

        Parametros:
        - variable: bool para indicar si se desea quitar un ambito de variables.
        - estructura: bool para indicar si se desea quitar un ambito de estructuras.
        - funcion: bool para indicar si se desea quitar un ambito de funciones.
        '''
        if variable:
            offsetLocal.pop()
            pilaVariable.pop()
        if estructura:
            pilaEstructura.pop()
        if funcion:
            pilaFuncion.pop()

    def agregarPropiedadesAPila(self, nombre):
        '''
        Funcion para crear un nuevo ambito y agregar las propiedades
        de una estructura al ultimo ambito

        Parametros:
        - nombre: nombre de la estructura
        '''
        self.agregarAmbito(variable=True, estructura=False, funcion=False)

        pilaVariable[-1].update(pilaEstructura[-1][nombre].propiedades)

    def validarReglaMain(self):
        try:
            if not(len(pilaFuncion[-1]['main'].argumentosTipos) == 0):
                return Error('La funcion main contiene parametros')
        except:
            # no existe main
            return Error('Programa sin funcion main')

    def visitar(self, tree):
        '''
        Funcion para visitar un arbol de antlr.

        Parametros:
        * tree: nodo raiz de antlr.

        Retorno:
        * Si la raiz tiene mas de un hijo retorna una lista con los resultados,
        caso contrario solo un resultado.
        '''
        if(isinstance(tree, list)):
            resultados = []
            for i in tree:
                resultados.append(self.visit(i))
            return resultados
        else:
            return self.visit(tree)

    def visitProgramStart(self, ctx: decafParser.ProgramStartContext):
        # se crea el ambito global
        self.agregarAmbito(variable=True, funcion=True, estructura=True)

        # visitamos todas las declaraciones del programa
        declaraciones = self.visitar(ctx.declaration())

        # validar Regla main
        err = self.validarReglaMain()
        if (isinstance(err, Error)):
            print(
                f"{FAIL}Error en linea {ctx.start.line}{ENDC}: {err.mensaje}")

        # se elimina ambito global
        self.quitarAmbito(variable=True, funcion=True, estructura=True)
        return declaraciones

    '''
    Declaracion de estructuras
    '''

    def visitStructDec(self, ctx: decafParser.StructDecContext):
        # se crea ambito de variable
        self.agregarAmbito()

        nombre = ctx.id_tok().getText()
        self.visitar(ctx.varDeclaration())

        errTemp = self.agregarStructATabla(
            nombre, Estructura(copy.deepcopy(pilaVariable[-1])))

        if (isinstance(errTemp, Error)):
            print(
                f"{FAIL}Error en declaracion de estructura linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")

        # se agrega el ancho de la estructura declarada
        ancho[nombre] = offsetLocal[-1]

        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    '''
    Manejo de metodos
    '''

    def procesarParametros(self, parametros):
        '''
        Funcion para procesar parametros y agregarlos al nuevo ambito

        Parametros:
        - parametros: lista de objeto <Nodo> con la informacion de cada parametro

        Return
        - <Error> si hay dos parametros iguales,
        - <Lista> de tipos de parametros caso contrario
        '''
        parametrosList = []
        for i in parametros:
            nombre = i.nombre
            try:
                long = int(i.isArray)**0
            except:
                long = None
            if (i.tipo != tipos.VOID):
                parametrosList.append(i.tipo)
                offset, isLocal = self.calcularOffset(i.tipo)
                variable = Variable(i.tipo, i.nombre, long,
                                    offset=offset, local=isLocal)
                errTemp = self.agregarVariableATabla(nombre, variable)
                if isinstance(errTemp, Error):
                    return Error(f"Parametro '{i.nombre}' ya existe")
        return parametrosList

    def agregarReturn(self, tipo):
        global nombreFuncionTemp
        pilaFuncion[-1][nombreFuncionTemp].retornoTipos.append(tipo)

    def visitMethodDec(self, ctx: decafParser.MethodDecContext):
        # se crea ambito de variable
        global nombreFuncionTemp
        self.agregarAmbito()

        nombre = ctx.id_tok().getText()
        tipo = ctx.methodType().getText()
        parametros = self.visitar(ctx.parameter())

        # agregar parametros al ambito
        paramErr = self.procesarParametros(parametros)
        if(isinstance(paramErr, Error)):
            print(
                f"{FAIL}Error en declaracion de funcion linea {ctx.start.line}{ENDC}: {paramErr.mensaje}")
            return

        nombreFuncionTemp = nombre
        # guardar la funcion en tabla
        self.agregarFuncionATabla(nombre, Funcion(tipo, paramErr))

        resultados = self.visitar(ctx.block())

        # validar declaracion de funcion
        pilaFuncion[-1][nombreFuncionTemp].validar()

        errTemp = pilaFuncion[-1][nombreFuncionTemp].err
        if(isinstance(errTemp, Error)):
            print(
                f"{FAIL}Error en declaracion de funcion linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")

        # se elimina ambito de variable
        self.quitarAmbito()

        # Codigo intermedio
        # Se agrega cuadruplas con etiquetas de funcion
        if(isinstance(resultados, list)):
            print('revisame')
            print(resultados)
        else:
            resultados.codigo.insert(0, Cuadrupla(op='FUNCTION', arg1=nombre))
            resultados.codigo.append(Cuadrupla(op='END FUNCTION', arg1=nombre))
        return resultados

    def visitIdParam(self, ctx: decafParser.IdParamContext):
        tipo = ctx.parameterType().getText()
        nombre = ctx.id_tok().getText()
        return Nodo(tipo, nombre)

    def visitVoidParam(self, ctx: decafParser.VoidParamContext):
        return Nodo(tipos.VOID)

    def visitArrayParam(self, ctx: decafParser.ArrayParamContext):
        tipo = ctx.parameterType().getText()
        nombre = ctx.id_tok().getText()
        return Nodo(tipo, nombre, True)

    def visitMethodCallDec(self, ctx: decafParser.MethodCallDecContext):
        nombre = ctx.id_tok().getText()
        tipo = tipos.getMethodType(nombre, pilaFuncion)

        # Se valida que exista la funcion
        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de funcion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.METHOD)

        # Se valida que los argumentos coincidan con la firma
        argumentos = self.visitar(ctx.arg())

        errTemp = tipos.validarTiposArgumentos(
            nombre, copy.deepcopy(argumentos), pilaFuncion)
        if (isinstance(errTemp, Error)):
            print(
                f"{FAIL}Error en llamada de funcion linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
            return Nodo(tipos.ERROR, tipos.METHOD)

        '''
            CODIGO INTERMEDIO
        '''
        retorno = Nodo(tipo, tipos.METHOD)
        retorno.direccion = 'R'

        for argumento in argumentos:
            retorno.codigo += argumento.codigo
            retorno.codigo.append(
                Cuadrupla(op='PARAM', arg1=argumento.direccion, tab=1))

        retorno.codigo.append(
            Cuadrupla(op='CALL', arg1=nombre, arg2=len(argumentos), tab=1))
        return retorno

    '''
    Declaracion de variable y arreglo
    '''

    def visitVarDec(self, ctx: decafParser.VarDecContext):
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        errTemp = None
        esEstructura = False

        # Validar si es de tipo estructura
        if (tipo.find('struct') != -1):
            # es de tipo estructura
            tipo = tipo.replace('struct', '')

            errTemp = self.validarEstructura(tipo)
            if (isinstance(errTemp, Error)):
                print(
                    f"{FAIL}Error en declaracion de variable linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
                return
            esEstructura = True

        # Calculo de offset y isLocal
        offset, isLocal = self.calcularOffset(tipo)

        errTemp = self.agregarVariableATabla(
            nombre, Variable(tipo, isEstructura=esEstructura, offset=offset, local=isLocal))
        if isinstance(errTemp, Error):
            print(
                f"{FAIL}Error en declaracion de variable linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
        return None

    def visitArrayDec(self, ctx: decafParser.ArrayDecContext):
        num = int(ctx.num().getText())
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        esEstructura = False

        # validar que num sea mayor a 0
        if not(num > 0):
            print(
                f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: la dimension debe ser mayor a 0")
            return

        # Validar si es de tipo estructura
        if (tipo.find('struct') != -1):
            # es de tipo estructura
            tipo = tipo.replace('struct', '')

            errTemp = self.validarEstructura(tipo)
            if (isinstance(errTemp, Error)):
                print(
                    f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
                return
            esEstructura = True

        # Calculo de offset y isLocal
        offset, isLocal = self.calcularOffset(tipo, num)

        errTemp = self.agregarVariableATabla(
            nombre, Variable(tipo, isEstructura=esEstructura, long=num, offset=offset, local=isLocal))
        if isinstance(errTemp, Error):
            print(
                f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")

        return None

    '''
    Manejo de literales
    '''

    def visitIntLiteral(self, ctx: decafParser.IntLiteralContext):
        # print('visitIntLiteral')
        # print(ctx.getText())
        return Nodo(tipos.INT, tipos.LITERAL, direccion=ctx.getText())

    def visitCharLiteral(self, ctx: decafParser.CharLiteralContext):
        # print('visitCharLiteral')
        # print(ctx.getText())
        return Nodo(tipos.CHAR, tipos.LITERAL, direccion=ctx.getText())

    def visitBoolLiteral(self, ctx: decafParser.BoolLiteralContext):
        # print('visitBoolLiteral')
        # print(ctx.getText())
        return Nodo(tipos.BOOLEAN, tipos.LITERAL, direccion=ctx.getText())

    '''
    Manejo de llamada de variables
    '''

    def visitIdLocation(self, ctx: decafParser.IdLocationContext):
        global offsetLocationDot
        global procesandoLocation
        global isLocationLocal
        global codigoLocation
        global ultimaDireccionLocation

        nombre = ctx.id_tok().getText()
        tipo = tipos.getidLocationType(nombre, pilaVariable)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.IDLOCATION)

        '''
            CODIGO INTERMEDIO
        '''
        retorno = Nodo(tipo, tipos.IDLOCATION)
        tempDir = None
        if (isinstance(ctx.parentCtx, (decafParser.IdLocationDotContext, decafParser.ArrayLocationDotContext))):

            offset = offsetLocationDot + self.getOffset(nombre)
            if (len(codigoLocation) > 0):
                retorno.codigo += codigoLocation
                retorno.codigo.append(
                    Cuadrupla(op='+', arg1=ultimaDireccionLocation, arg2=offset, resultado=ultimaDireccionLocation, tab=1))
                if (isLocationLocal):
                    tempDir = f'FP[{ultimaDireccionLocation}]'
                else:
                    tempDir = f'G[{ultimaDireccionLocation}]'
            else:
                if (isLocationLocal):
                    tempDir = f'FP[{offset}]'
                else:
                    tempDir = f'G[{offset}]'

            offsetLocationDot = 0
            procesandoLocation = False
            codigoLocation = []
            ultimaDireccionLocation = None
        else:
            tempDir = self.generarTemporal(nombre)
        retorno.direccion = tempDir
        return retorno

    def visitArrayLocation(self, ctx: decafParser.ArrayLocationContext):
        nombre = ctx.id_tok().getText()
        expression = self.visitar(ctx.expression())

        # se valida que la variable exista y sea array
        tipo = tipos.getArrayLocationType(nombre, pilaVariable)
        if(isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

        retorno = None
        # Se valida que expression sea de tipo int
        if (expression.tipo == tipos.INT):
            retorno = Nodo(tipo, tipos.ARRAYLOCATION)
        else:
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: exp no es de tipo 'int'")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

        '''
            CODIGO INTERMEDIO
        '''
        indexTemp = self.nuevaTemporal()
        returnTemp = self.nuevaTemporal()
        retorno.direccion = self.generarTemporalArray(nombre, returnTemp)

        retorno.codigo += expression.codigo

        retorno.codigo.append(
            Cuadrupla(op='*', arg1=ancho[tipo], arg2=expression.direccion, resultado=indexTemp, tab=1))

        offset = self.getOffset(nombre)
        retorno.codigo.append(
            Cuadrupla(op='+', arg1=offset, arg2=indexTemp, resultado=returnTemp, tab=1))

        return retorno

    def visitIdLocationDot(self, ctx: decafParser.IdLocationDotContext):
        global offsetLocationDot
        global procesandoLocation
        global isLocationLocal
        nombre = ctx.id_tok().getText()

        # se valida que la variable sea de tipo estructura
        tipoEstructura = tipos.validarEstructura(nombre, pilaVariable)
        if(isinstance(tipoEstructura, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipoEstructura.mensaje}")
            return Nodo(tipos.ERROR, tipos.IDLOCATIONDOT)

        # se hace push a la pila de variables con las propiedades de la struct
        self.agregarPropiedadesAPila(tipoEstructura)

        if not procesandoLocation:
            procesandoLocation = True
            isLocationLocal = self.getIsLocal()

        offsetLocationDot += self.getOffset(nombre)

        tipo = self.visitar(ctx.location())

        # se hace pop a la pila de variables con las propiedades de la struct
        self.quitarAmbito(variable=True, estructura=False, funcion=False)

        return tipo

    def visitArrayLocationDot(self, ctx: decafParser.ArrayLocationDotContext):
        global procesandoLocation
        global isLocationLocal
        global offsetLocationDot
        global codigoLocation
        global ultimaDireccionLocation

        nombre = ctx.id_tok().getText()

        # se valida que la variable sea de tipo estructura y sea un array
        tipoEstructura = tipos.validarEstructuraArray(nombre, pilaVariable)
        if(isinstance(tipoEstructura, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipoEstructura.mensaje}")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATIONDOT)

        # validar que exp sea de tipo int
        tipoExp = self.visitar(ctx.expression())
        if (tipoExp.tipo != tipos.INT):
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: exp no es de tipo 'int'")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATIONDOT)

        # se hace push a la pila de variables con las propiedades de la struct
        self.agregarPropiedadesAPila(tipoEstructura)

        '''
            CODIGO INTERMEDIO
        '''
        if not procesandoLocation:
            procesandoLocation = True
            isLocationLocal = self.getIsLocal()

        structTipo = tipos.getArrayLocationType(nombre, pilaVariable)
        try:
            offset = self.getOffset(nombre)
            offset += int(tipoExp.direccion) * ancho[structTipo]
            offsetLocationDot += offset
        except:
            # ultimaDireccionLocation =
            offset = self.getOffset(nombre)

            codigoLocation += tipoExp.codigo

            direccionTemp = self.nuevaTemporal()
            codigoLocation.append(
                Cuadrupla(op='*', arg1=tipoExp.direccion, arg2=ancho[structTipo], resultado=direccionTemp, tab=1))

            if (ultimaDireccionLocation != None):
                codigoLocation.append(
                    Cuadrupla(op='+', arg1=direccionTemp, arg2=ultimaDireccionLocation, resultado=direccionTemp, tab=1))

            ultimaDireccionLocation = direccionTemp

        tipo = self.visitar(ctx.location())

        # se hace pop a la pila de variables con las propiedades de la struct
        self.quitarAmbito(variable=True, estructura=False, funcion=False)

        return tipo

    '''
    Manejo de statement
    '''

    def visitAssignmentStmt(self, ctx: decafParser.AssignmentStmtContext):
        location = self.visitar(ctx.location())
        expression = self.visitar(ctx.expression())
        tipo = tipos.validarTiposAsignacion(expression, location)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en asignacion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.ASSIGNMENT)
        else:
            '''
                CODIGO INTERMEDIO
            '''
            retorno = Nodo(tipo, tipos.ASSIGNMENT)
            retorno.codigo += expression.codigo
            retorno.codigo += location.codigo
            retorno.codigo.append(
                Cuadrupla(op='=',
                          resultado=location.direccion,
                          arg1=expression.direccion,
                          tab=1
                          ))
            return retorno

    def visitIfStmt(self, ctx: decafParser.IfStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()
        resultado = Nodo(tipos.VOID, tipos.IFBLOCK)

        exp = self.visitar(ctx.expression())

        if (exp.tipo != tipos.BOOLEAN):
            print(
                f"{FAIL}Error en expresion de if linea {ctx.start.line}{ENDC}: no es de tipo boolean")
        bloque = self.visitar(ctx.block())

        # se elimina ambito de variable
        self.quitarAmbito()

        '''
        Codigo intermedio
        '''

        resultado.etiquetaTrue = self.nuevaEtiqueta('true')
        endIf = self.nuevaEtiqueta('endIf')

        resultado.codigo += exp.codigo

        resultado.codigo.append(Cuadrupla(op='IF', arg1=f'{exp.direccion}>0', arg2='GOTO',
                                          resultado=resultado.etiquetaTrue, tab=1))

        resultado.codigo.append(
            Cuadrupla(op='GOTO', arg1=endIf, tab=1))

        resultado.codigo.append(
            Cuadrupla(op=resultado.etiquetaTrue, tab=0))

        resultado.codigo += bloque.codigo

        resultado.codigo.append(Cuadrupla(op=endIf, tab=0))

        return resultado

    def visitIfElseStmt(self, ctx: decafParser.IfElseStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()
        resultado = Nodo(tipos.VOID, tipos.IFBLOCK)

        exp = self.visitar(ctx.expression())

        if (exp.tipo != tipos.BOOLEAN):
            print(
                f"{FAIL}Error en expresion de if linea {ctx.start.line}{ENDC}: no es de tipo boolean")
        bloques = self.visitar(ctx.block())

        # se elimina ambito de variable
        self.quitarAmbito()

        '''
        Codigo intermedio
        '''
        # print(f'bloques {bloques}')

        resultado.etiquetaTrue = self.nuevaEtiqueta('true')
        resultado.etiquetaFalse = self.nuevaEtiqueta('false')
        endIf = self.nuevaEtiqueta('endIf')

        resultado.codigo += exp.codigo

        resultado.codigo.append(Cuadrupla(op='IF', arg1=f'{exp.direccion}>0', arg2='GOTO',
                                          resultado=resultado.etiquetaTrue, tab=1))

        resultado.codigo.append(
            Cuadrupla(op='GOTO', arg1=resultado.etiquetaFalse, tab=1))

        resultado.codigo.append(
            Cuadrupla(op=resultado.etiquetaTrue, tab=0))

        resultado.codigo += bloques[0].codigo

        resultado.codigo.append(
            Cuadrupla(op='GOTO', arg1=endIf, tab=1))

        resultado.codigo.append(
            Cuadrupla(op=resultado.etiquetaFalse, tab=0))

        resultado.codigo += bloques[1].codigo

        resultado.codigo.append(Cuadrupla(op=endIf, tab=0))

        return resultado

    def visitWhileStmt(self, ctx: decafParser.WhileStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        exp = self.visitar(ctx.expression())

        if (exp.tipo != tipos.BOOLEAN):
            print(
                f"{FAIL}Error en expresion de while linea {ctx.start.line}{ENDC}: no es de tipo boolean")
        bloque = self.visitar(ctx.block())

        # se elimina ambito de variable
        self.quitarAmbito()
        retorno = Nodo(tipos.VOID, tipos.WHILE)
        '''
            Codigo Intermedio
        '''
        inicio = self.nuevaEtiqueta('startWhile')
        exp.etiquetaTrue = self.nuevaEtiqueta('true')
        exp.etiquetaFalse = self.nuevaEtiqueta('endWhile')

        retorno.codigo.append(Cuadrupla(op=inicio, tab=0))

        retorno.codigo += exp.codigo

        retorno.codigo.append(Cuadrupla(op='IF', arg1=f'{exp.direccion}>0',
                                        arg2='GOTO', resultado=exp.etiquetaTrue, tab=1))

        retorno.codigo.append(
            Cuadrupla(op='GOTO', arg1=exp.etiquetaFalse, tab=1))

        retorno.codigo.append(Cuadrupla(op=exp.etiquetaTrue, tab=0))

        retorno.codigo += bloque.codigo

        retorno.codigo.append(Cuadrupla(op='GOTO', arg1=inicio, tab=1))

        retorno.codigo.append(Cuadrupla(op=exp.etiquetaFalse, tab=0))

        return retorno

    def visitReturnStmt(self, ctx: decafParser.ReturnStmtContext):
        returnNodo = Nodo(tipos.VOID, tipos.RETURN)
        exp = None
        try:
            exp = self.visitar(ctx.expression())
            self.agregarReturn(exp.tipo)
        except:
            print('err')
            pass
        '''
            CODIGO INTERMEDIO
        '''
        returnNodo.codigo += exp.codigo

        returnNodo.codigo.append(
            Cuadrupla(op='RETURN', arg1=exp.direccion, tab=1))

        return returnNodo

    '''
    Manejo de expresiones
    '''

    def manejarOperaciones(self, expres, ctx, tipoResultado, tipoOperandos):
        '''
        Funcion para manejar operaciones de tipo Arith '*'|'/'|'%'|'+'|'-'
        y tambien de tipo Rel '<'|'>'|'<='|'>='

        Parametros:
        - expres: lista de <Nodos>
        - ctx: contexto de la funcion donde se llama el metodo
        - tipoResultado: si la operacion sale bien, que tipo es el resultado

        Return:
        - objeto tipo <Nodo> con el resultado
        '''
        tipo = tipos.validarTiposOperacion(expres)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.OPERACION)

        else:
            if(tipo != tipoOperandos):
                print(
                    f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: No se puede usar el operador '{ctx.op.text}' con tipos de dato '{tipo}'")
                return Nodo(tipos.ERROR, tipos.OPERACION)
        '''
        CODIGO INTERMEDIO
        '''
        dirTemp = self.nuevaTemporal()
        retorno = Nodo(tipoResultado, tipos.OPERACION, direccion=dirTemp)
        if (isinstance(expres, list)):
            # si es operacion con dos expresiones
            retorno.codigo += expres[0].codigo
            retorno.codigo += expres[1].codigo

            retorno.codigo.append(
                Cuadrupla(resultado=dirTemp,
                          arg1=expres[0].direccion,
                          arg2=expres[1].direccion,
                          op=ctx.op.text,
                          tab=1)
            )
        else:
            # si es operacion con una expresion
            retorno.codigo.append(expres.codigo)
            retorno.codigo.append(
                Cuadrupla(resultado=dirTemp,
                          arg1=0,
                          arg2=expres.direccion,
                          op=ctx.op.text,
                          tab=1)
            )
        return retorno

    def visitFirstArithExpr(self, ctx: decafParser.FirstArithExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitSecondArithExpr(self, ctx: decafParser.SecondArithExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitRelExpr(self, ctx: decafParser.RelExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.INT)

    def visitEqExpr(self, ctx: decafParser.EqExprContext):
        expres = self.visitar(ctx.expression())
        tipo = tipos.validarTiposOperacion(expres)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.OPERACION)

        '''
        CODIGO INTERMEDIO
        '''
        dirTemp = self.nuevaTemporal()
        retorno = Nodo(tipos.BOOLEAN, tipos.OPERACION, direccion=dirTemp)

        retorno.codigo += expres[0].codigo
        retorno.codigo += expres[1].codigo
        retorno.codigo.append(
            Cuadrupla(resultado=dirTemp,
                      arg1=expres[0].direccion,
                      arg2=expres[1].direccion,
                      op=ctx.op.text,
                      tab=1)
        )
        return retorno

    def visitCondExpr(self, ctx: decafParser.CondExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.BOOLEAN)

    def visitNegativeExpr(self, ctx: decafParser.NegativeExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitNotExpr(self, ctx: decafParser.NotExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.BOOLEAN)

    def visitParExpr(self, ctx: decafParser.ParExprContext):
        return self.visitar(ctx.expression())

    '''
        Manejo de bloque
    '''

    def visitBlockDec(self, ctx: decafParser.BlockDecContext):
        resultado = Nodo(tipos.VOID, tipos.BLOQUE)
        self.visitar(ctx.varDeclaration())

        statements = self.visitar(ctx.statement())
        # print(f'statements {statements}')
        for statement in statements:
            try:
                resultado.codigo += statement.codigo
            except:
                pass
        # print(f'resultado {resultado}')
        return resultado


def aprocesarCodigo(nodo):
    if (isinstance(nodo, list)):
        for i in nodo:
            aprocesarCodigo(i)
    else:
        print(nodo)


def procesarNodo(nodo):
    if (isinstance(nodo, list)):
        for i in nodo:
            procesarNodo(i)
    else:
        aprocesarCodigo(nodo.codigo)


def main():
    data = open('../decafPrograms/hello_world.txt').read()
    lexer = decafLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = decafParser(stream)
    tree = parser.start()
    nodos = EvalVisitor().visit(tree)

    codigoIntermedio = []
    for nodo in nodos:
        if nodo != None:
            codigoIntermedio.append(nodo)

    for linea in codigoIntermedio:
        procesarNodo(linea)


if __name__ == '__main__':
    main()
