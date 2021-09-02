from Estructura import Estructura
from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from decafLexer import decafLexer
from decafListener import decafListener
from decafParser import decafParser
from Variable import *
from Funcion import *
from Tipos import *
from Error import *
import copy
import sys

pilaVariable = []
pilaFuncion = []
pilaEstructura = []
funcionTemp = None
funcionNombreTemp = None

procesandoReturnExp = False
expressionReturnTemp = []

procesandoArrayExp = False
expressionArrayTemp = []

'''
Aqui se guardan los parametros de la funcion
para luego al entrar al ambito de la funcion
ingresar esas variables
'''
ambitoVariableTemp = {}


class DecafPrinter(decafListener):
    def __init__(self) -> None:
        super().__init__()

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
        if(nombre in pilaEstructura[-1].keys()):
            return 'Esta estructura ya existe'
        else:
            pilaEstructura[-1][nombre] = estructura

        print(f'''
                # Pila Estructura
                {pilaEstructura}
                ''')

    def agregarVariableAmbitoTemp(self, nombre, variable):
        '''
        Funcion que valida si una variable ya existe en el ambito temporal
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        El ambito temporal se crea para registrar los parametros de una funcion, antes
        de ingresar al block donde se crea el verdadero ambito.

        Parametros
        - nombre: string con el nombre de la variable
        - variable: objeto Variable con la informacion de la variable a ingresar.
        '''
        if(nombre in ambitoVariableTemp.keys()):
            return f'La variable "{nombre}" ya existe dentro de los parametros de la funcion'
        else:
            ambitoVariableTemp[nombre] = variable

        print(f'''
                # Pila Variables [temp]
                {ambitoVariableTemp}
                ''')

    def agregarAmbitoTempATabla(self):
        '''
        Pasa el ambitoTemp al ambito de la funcion y limpia
        el ambitoTemp.
        No retorna nada
        '''
        global ambitoVariableTemp
        pilaVariable[-1].update(ambitoVariableTemp)
        ambitoVariableTemp = {}

        print(f'''
                # Pila Variables
                {pilaVariable}
                ''')

    def validarReglaMain(self):
        try:
            if not(len(pilaFuncion[-1]['main'].argumentosTipos) == 0):
                return Error('La funcion main contiene parametros')
        except:
            # no existe main
            return Error('Programa sin funcion main')

    def agregarAmbito(self):
        pilaVariable.append({})
        pilaEstructura.append({})

    def quitarAmbito(self):
        pilaVariable.pop()
        pilaEstructura.pop()

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

            print(f'''
                    # Pila funciones
                    {pilaFuncion}
                    ''')

    def procesarParametros(self, parametros):
        '''
        Funcion para procesar parametros, valida si tiene de parametro void
        no puede ir acompañado de mas tipos.

        Parametros
        - parametros: lista de nodos tipo parameter
        '''
        parametrosList = []

        # revisa si contiene de parametros void, no puede ir acompañado de más tipos
        if (parametros[0].getText() == 'void'):
            if (len(parametros) == 1):
                return parametrosList
            else:
                return Error('parametro void no puede ir acompañado de mas parametros')

        for i in parametros:
            nombre = i.id_tok().getText()
            tipo = i.parameterType().getText()

            # Se agregan parametros a la tabla del ambito de esta funcion
            declaracionTemp = self.agregarVariableAmbitoTemp(
                nombre, Variable(tipo))
            if (declaracionTemp):
                return declaracionTemp

            parametrosList.append(tipo)

        return parametrosList

    def enterMethodDec(self, ctx: decafParser.MethodDecContext):
        global funcionTemp
        global funcionNombreTemp
        tipo = ctx.methodType().getText()
        nombre = ctx.id_tok().getText()
        parametros = []

        if(len(ctx.parameter()) > 0):
            # Hay parametros
            parametros = self.procesarParametros(ctx.parameter())

            if (isinstance(parametros, Error)):
                # hay error
                print(
                    f"Error en declaracion de funcion linea {ctx.start.line}: {parametros.mensaje}")

        funcionTemp = copy.deepcopy(Funcion(tipo, parametros))
        funcionNombreTemp = nombre

    def enterReturnStmt(self, ctx: decafParser.ReturnStmtContext):
        global procesandoReturnExp
        procesandoReturnExp = True

    def enterIntLiteral(self, ctx: decafParser.IntLiteralContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('int')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('int')

    def enterCharLiteral(self, ctx: decafParser.CharLiteralContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('char')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('char')

    def enterBoolLiteral(self, ctx: decafParser.BoolLiteralContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('boolean')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('boolean')

    # TODO expression con idLocationDot, arrayLocationDot
    def enterArrayLocation(self, ctx: decafParser.ArrayLocationContext):
        global procesandoArrayExp
        global expressionArrayTemp

        procesandoArrayExp = True

    def exitArrayLocation(self, ctx: decafParser.ArrayLocationContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp
        # se validan los tipos y se agregan en arrays correspondientes
        nombre = ctx.id_tok().getText()
        expType = procesarExp(expressionArrayTemp)
        tipo = getArrayLocationType(nombre, pilaVariable, expType)

        if (procesandoReturnExp):
            if (isinstance(tipo, Error)):
                print(
                    f"Error en llamada de array linea {ctx.start.line}: {tipo.mensaje}")
                expressionReturnTemp.append('err')
            else:
                expressionReturnTemp.append(tipo)

        procesandoArrayExp = False
        expressionArrayTemp = []

    def enterIdLocation(self, ctx: decafParser.IdLocationContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        tipo = getidLocationType(ctx.id_tok().getText(), pilaVariable)

        if (procesandoArrayExp):
            if (isinstance(tipo, Error)):
                print(
                    f"Error en llamada de variable linea {ctx.start.line}: {tipo.mensaje}")
                expressionArrayTemp.append('err')
            else:
                expressionArrayTemp.append(tipo)

        elif (procesandoReturnExp):
            if (isinstance(tipo, Error)):
                print(
                    f"Error en llamada de variable linea {ctx.start.line}: {tipo.mensaje}")
                expressionReturnTemp.append('err')
            else:
                expressionReturnTemp.append(tipo)

    def enterMethodCallDec(self, ctx: decafParser.MethodCallDecContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        tipo = getMethodType(ctx.id_tok().getText(), pilaFuncion)

        if (procesandoArrayExp):
            if (isinstance(tipo, Error)):
                print(
                    f"Error en llamada de funcion linea {ctx.start.line}: {tipo.mensaje}")
                expressionArrayTemp.append('err')
            else:
                expressionArrayTemp.append(tipo)

        elif (procesandoReturnExp):
            if (isinstance(tipo, Error)):
                print(
                    f"Error en llamada de funcion linea {ctx.start.line}: {tipo.mensaje}")
                expressionReturnTemp.append('err')
            else:
                expressionReturnTemp.append(tipo)

    def enterNegativeExpr(self, ctx: decafParser.NegativeExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('negative')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('negative')

    def enterNotExpr(self, ctx: decafParser.NotExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('not')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('not')

    def enterFirstArithExpr(self, ctx: decafParser.FirstArithExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('intOp')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('intOp')

    def enterSecondArithExpr(self, ctx: decafParser.SecondArithExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('intOp')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('intOp')

    def enterRelExpr(self, ctx: decafParser.RelExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('relOp')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('relOp')

    def enterEqExpr(self, ctx: decafParser.EqExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('eqOp')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('eqOp')

    def enterCondExpr(self, ctx: decafParser.CondExprContext):
        global procesandoReturnExp
        global expressionReturnTemp

        global procesandoArrayExp
        global expressionArrayTemp

        if (procesandoArrayExp):
            expressionArrayTemp.append('boolOp')

        elif (procesandoReturnExp):
            expressionReturnTemp.append('boolOp')

    def exitReturnStmt(self, ctx: decafParser.ReturnStmtContext):
        global procesandoReturnExp
        global funcionTemp
        global expressionReturnTemp
        print(f'''
        -----
        exitReturnStatement {ctx.start.line}
        -----
        expressionReturnTemp {expressionReturnTemp}
        ''')
        funcionTemp.agregarReturn(procesarExp(expressionReturnTemp))
        expressionReturnTemp = []
        procesandoReturnExp = False

    def exitMethodDec(self, ctx: decafParser.MethodDecContext):
        global funcionTemp
        global funcionNombreTemp
        global procesandoReturnExp
        global expressionReturnTemp

        funcionTemp.validar()
        if (isinstance(funcionTemp.err, Error)):
            # si hay error en definicion de funcion
            print(
                f"Error en declaracion de funcion linea {ctx.start.line}: {funcionTemp.err.mensaje}")
        else:
            # si no hay error se agrega a tabla
            err = self.agregarFuncionATabla(funcionNombreTemp, funcionTemp)
            if (isinstance(err, Error)):
                print(
                    f"Error en declaracion de funcion linea {ctx.start.line}: {err.mensaje}")

        funcionTemp = None
        funcionNombreTemp = None

    def enterVarDec(self, ctx: decafParser.VarDecContext):
        # es la declaracion de una variable
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        declaracionTemp = self.agregarVariableATabla(
            nombre, Variable(tipo))
        if(isinstance(declaracionTemp, Error)):
            print(
                f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp.mensaje}")

    def enterArrayDec(self, ctx: decafParser.ArrayDecContext):
        # es la declaracion de un array
        long = int(ctx.children[3].getText())
        if(long <= 0):
            print(
                f"Error en declaracion de array linea {ctx.start.line}: la dimension debe ser mayor a 0")
        else:
            nombre = ctx.id_tok().getText()
            tipo = ctx.varType().getText()
            declaracionTemp = self.agregarVariableATabla(
                nombre, Variable(tipo, long=long))
            if(isinstance(declaracionTemp, Error)):
                print(
                    f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp.mensaje}")

    def enterProgramStart(self, ctx: decafParser.ProgramStartContext):
        # Se crea el ambito global
        self.agregarAmbito()
        pilaFuncion.append({})

    def enterStructDec(self, ctx: decafParser.StructDecContext):
        self.agregarAmbito()

    def exitStructDec(self, ctx: decafParser.StructDecContext):
        # pasar este ambito a las propiedades de la estructura
        nombre = ctx.id_tok().getText()
        self.agregarStructATabla(nombre, Estructura(
            copy.deepcopy(pilaVariable[-1])))
        self.quitarAmbito()

    def enterBlockDec(self, ctx: decafParser.BlockDecContext):
        self.agregarAmbito()
        if (len(ambitoVariableTemp) > 0):
            self.agregarAmbitoTempATabla()

    def exitBlockDec(self, ctx: decafParser.BlockDecContext):
        self.quitarAmbito()

    def exitProgramStart(self, ctx: decafParser.ProgramStartContext):
        # este metodo se ejecuta al salir del ultimo nodo del arbol
        reglaMain = self.validarReglaMain()
        if (isinstance(reglaMain, Error)):
            print(
                f"Error en linea {ctx.start.line}: {reglaMain.mensaje}")


def main():
    print("Listo")
    data = open('./decafPrograms/hello_world.txt').read()
    lexer = decafLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = decafParser(stream)
    tree = parser.start()

    printer = DecafPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    # traverse(tree, parser.ruleNames)

    # print(tree.getText())
    # print(tree.getRuleIndex())
    # print(parser.ruleNames)

    # print(tree.getChild(1))

    # print(tree.getToken(3, 0))
    # print(tree.getTokens(3))

    print()


if __name__ == '__main__':
    main()
