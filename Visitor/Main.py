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

# codigo intermedio
codigoIntermedio = []

# contador de temporales
contadorTemporales = 0

FAIL = '\033[91m'
ENDC = '\033[0m'

nombreFuncionTemp = ""


class EvalVisitor(decafVisitor):

    def calcularOffset(self, tipo):
        '''
            Funcion para calcular el offset de una
            variable segun el tipo.

            Parametros:
            - tipo: tipo de variable

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
                offsetLocal[-1] += ancho[tipo]
            else:
                # sino es offsetGlobal
                isLocal = False
                offset = offsetGlobal
                offsetGlobal += ancho[tipo]
        except:
            pass

        return offset, isLocal

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
        # TODO manejar arreglos, estructuras
        for i in range(len(pilaVariable) - 1, -1, -1):
            ambito = pilaVariable[i]
            if(nombre in ambito.keys()):

                offset = ambito[nombre].offset

                if (ambito[nombre].isLocal):
                    return f"fp[{offset}]"
                else:
                    return f"G[{offset}]"

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
        return codigoIntermedio

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
                variable = Variable(i.tipo, i.nombre, long)
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
        return ctx.id_tok().getText()

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

        errTemp = tipos.validarTiposArgumentos(nombre, argumentos, pilaFuncion)
        if (isinstance(errTemp, Error)):
            print(
                f"{FAIL}Error en llamada de funcion linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
            return Nodo(tipos.ERROR, tipos.METHOD)

        return Nodo(tipo, tipos.METHOD)

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

        errTemp = self.agregarVariableATabla(
            nombre, Variable(tipo, isEstructura=esEstructura, long=num))
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
        return Nodo(tipos.INT, tipos.LITERAL)

    def visitCharLiteral(self, ctx: decafParser.CharLiteralContext):
        # print('visitCharLiteral')
        # print(ctx.getText())
        return Nodo(tipos.CHAR, tipos.LITERAL)

    def visitBoolLiteral(self, ctx: decafParser.BoolLiteralContext):
        # print('visitBoolLiteral')
        # print(ctx.getText())
        return Nodo(tipos.BOOLEAN, tipos.LITERAL)

    '''
    Manejo de llamada de variables
    '''

    def visitIdLocation(self, ctx: decafParser.IdLocationContext):
        nombre = ctx.id_tok().getText()
        tipo = tipos.getidLocationType(nombre, pilaVariable)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.IDLOCATION)

        tempDir = self.generarTemporal(nombre)
        return Nodo(tipo, tipos.IDLOCATION, direccion=tempDir)

    def visitArrayLocation(self, ctx: decafParser.ArrayLocationContext):
        nombre = ctx.id_tok().getText()
        expression = self.visitar(ctx.expression())

        # se valida que la variable exista y sea array
        tipo = tipos.getArrayLocationType(nombre, pilaVariable)
        if(isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

        # Se valida que expression sea de tipo int
        if (expression.tipo == tipos.INT):
            return Nodo(tipo, tipos.ARRAYLOCATION)
        else:
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: exp no es de tipo 'int'")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

    def visitIdLocationDot(self, ctx: decafParser.IdLocationDotContext):
        nombre = ctx.id_tok().getText()

        # se valida que la variable sea de tipo estructura
        tipoEstructura = tipos.validarEstructura(nombre, pilaVariable)
        if(isinstance(tipoEstructura, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipoEstructura.mensaje}")
            return Nodo(tipos.ERROR, tipos.IDLOCATIONDOT)

        # se hace push a la pila de variables con las propiedades de la struct
        self.agregarPropiedadesAPila(tipoEstructura)

        tipo = self.visitar(ctx.location())

        # se hace pop a la pila de variables con las propiedades de la struct
        self.quitarAmbito(variable=True, estructura=False, funcion=False)

        return tipo

    def visitArrayLocationDot(self, ctx: decafParser.ArrayLocationDotContext):
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
            resultadoTemp = self.generarTemporal(ctx.location().getText())
            codigoIntermedio.append(
                Cuadrupla(op='=',
                          resultado=resultadoTemp,
                          arg1=expression.direccion
                          ))
            return Nodo(tipo, tipos.ASSIGNMENT)

    def visitIfStmt(self, ctx: decafParser.IfStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        exp = self.visitar(ctx.expression())

        if (exp.tipo != tipos.BOOLEAN):
            print(
                f"{FAIL}Error en expresion de if linea {ctx.start.line}{ENDC}: no es de tipo boolean")
        self.visitar(ctx.block())
        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    def visitWhileStmt(self, ctx: decafParser.WhileStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        exp = self.visitar(ctx.expression())

        if (exp.tipo != tipos.BOOLEAN):
            print(
                f"{FAIL}Error en expresion de while linea {ctx.start.line}{ENDC}: no es de tipo boolean")
        self.visitar(ctx.block())

        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    def visitReturnStmt(self, ctx: decafParser.ReturnStmtContext):

        try:
            returnNodo = self.visitar(ctx.expression())
            self.agregarReturn(returnNodo.tipo)
        except:
            print('err')
            pass
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

        if (isinstance(expres, list)):
            # si es operacion con dos expresiones
            codigoIntermedio.append(
                Cuadrupla(resultado=dirTemp,
                          arg1=expres[0].direccion,
                          arg2=expres[1].direccion,
                          op=ctx.op.text)
            )
        else:
            # si es operacion con una expresion
            codigoIntermedio.append(
                Cuadrupla(resultado=dirTemp,
                          arg1=0,
                          arg2=expres.direccion,
                          op=ctx.op.text)
            )
        return Nodo(tipoResultado, tipos.OPERACION, direccion=dirTemp)

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

        return Nodo(tipos.BOOLEAN, tipos.OPERACION)

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


def main():
    data = open('../decafPrograms/hello_world.txt').read()
    lexer = decafLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = decafParser(stream)
    tree = parser.start()
    codigoIntermedio = EvalVisitor().visit(tree)

    for linea in codigoIntermedio:
        print(linea)


if __name__ == '__main__':
    main()
