from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from decafLexer import decafLexer
from decafListener import decafListener
from decafParser import decafParser
from Variable import *
from Funcion import *
from Tipos import *
import copy
import sys

pilaVariable = []
pilaFuncion = []
pilaEstructura = []
funcionTemp = None
funcionNombreTemp = None
procesandoExp = False
expressionTemp = []

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
            return 'Esta variable ya existe'
        else:
            pilaVariable[-1][nombre] = variable

        print(f'''
                # Pila Variables
                {pilaVariable}
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
                return 'La funcion main contiene parametros'
        except:
            # no existe main
            return 'Programa sin funcion main'

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
                return 'Esta funcion ya existe'
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
                return 'parametro void no puede ir acompañado de mas parametros'

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

            if (isinstance(parametros, str)):
                # hay error
                print(
                    f"Error en declaracion de funcion linea {ctx.start.line}: {parametros}")

        funcionTemp = copy.deepcopy(Funcion(tipo, parametros))
        funcionNombreTemp = nombre

    def enterReturnStmt(self, ctx: decafParser.ReturnStmtContext):
        global procesandoExp
        procesandoExp = True

    def enterIntLiteral(self, ctx: decafParser.IntLiteralContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            expressionTemp.append('int')

    def enterCharLiteral(self, ctx: decafParser.CharLiteralContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            expressionTemp.append('char')

    def enterBoolLiteral(self, ctx: decafParser.BoolLiteralContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            expressionTemp.append('boolean')

    # TODO expression con location, methodCall, -, !

    def enterFirstArithExpr(self, ctx: decafParser.FirstArithExprContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            # arith_op
            # if(ctx.op()):
            expressionTemp.append('intOp')

    def enterSecondArithExpr(self, ctx: decafParser.SecondArithExprContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            # arith_op
            # if(ctx.op()):
            expressionTemp.append('intOp')

    def enterRelExpr(self, ctx: decafParser.RelExprContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            # rel_op
            # if(ctx.op()):
            expressionTemp.append('relOp')

    def enterEqExpr(self, ctx: decafParser.EqExprContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            # eq_op
            # if(ctx.op()):
            expressionTemp.append('eqOp')

    def enterCondExpr(self, ctx: decafParser.CondExprContext):
        global procesandoExp
        global expressionTemp

        if (procesandoExp):
            # cond_op
            # if(ctx.op()):
            expressionTemp.append('boolOp')

    def exitReturnStmt(self, ctx: decafParser.ReturnStmtContext):
        global procesandoExp
        global funcionTemp
        global expressionTemp
        print(f'''
        -----
        exitReturnStatement {ctx.start.line}
        -----
        expressionTemp {expressionTemp}
        ''')
        funcionTemp.agregarReturn(procesarExp(expressionTemp))
        expressionTemp = []
        procesandoExp = False

    def exitMethodDec(self, ctx: decafParser.MethodDecContext):
        global funcionTemp
        global funcionNombreTemp
        global procesandoExp
        global expressionTemp

        funcionTemp.validar()
        if (funcionTemp.err):
            # si hay error en definicion de funcion
            print(
                f"Error en declaracion de funcion linea {ctx.start.line}: {funcionTemp.err}")
        else:
            # si no hay error se agrega a tabla
            self.agregarFuncionATabla(funcionNombreTemp, funcionTemp)

        funcionTemp = None
        funcionNombreTemp = None

    def enterVarDec(self, ctx: decafParser.VarDecContext):
        # es la declaracion de una variable
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        declaracionTemp = self.agregarVariableATabla(
            nombre, Variable(tipo))
        if(declaracionTemp):
            print(
                f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp}")

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
            if(declaracionTemp):
                print(
                    f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp}")

    def enterProgramStart(self, ctx: decafParser.ProgramStartContext):
        # Se crea el ambito global
        self.agregarAmbito()
        pilaFuncion.append({})

    def enterStructDec(self, ctx: decafParser.StructDecContext):
        self.agregarAmbito()

    def exitStructDec(self, ctx: decafParser.StructDecContext):
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
        if (reglaMain):
            print(
                f"Error en linea {ctx.start.line}: {reglaMain}")


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
