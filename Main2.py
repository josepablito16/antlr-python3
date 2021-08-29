from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from decafLexer import decafLexer
from decafListener import decafListener
from decafParser import decafParser
from Variable import *
from Funcion import *
import sys

pilaVariable = []
pilaFuncion = []
pilaEstructura = []
funcionTemp = None
funcionNombreTemp = None
procesandoReturn = False
retrunArray = []


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
                pilaFuncion[-1][nombre] = funcion

            print(f'''
                    # Pila funciones
                    {pilaFuncion}
                    ''')

    def procesarParametros(self, parametros):
        '''
        Funcion que valida si una funcion ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Parametros
        - nombre: string con el nombre de la funcion
        - funcion: objeto Funcion con la informacion de la funcion a ingresar.
        '''
        parametrosList = []

        if (parametros[0].getText() == 'void'):
            if (len(parametros) == 1):
                return parametrosList
            else:
                return 'parametro void no puede ir acompañado de mas parametros'

        for i in parametros:
            nombre = i.id_tok().getText()
            tipo = i.parameterType().getText()
            # TODO: agregar estos parametros a la tabla del ambito de esta funcion
            parametrosList.append(tipo)

        return parametrosList

    def enterMethodDeclaration(self, ctx: decafParser.MethodDeclarationContext):
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

        funcionTemp = Funcion(tipo, parametros)
        funcionNombreTemp = nombre

    def enterReturnStatement(self, ctx: decafParser.ReturnStatementContext):
        global procesandoReturn
        procesandoReturn = True

    def enterExpression(self, ctx: decafParser.ExpressionContext):
        global funcionTemp
        global procesandoReturn
        global retrunArray

        if (procesandoReturn):
            # location
            # TODO
            location = ctx.location()
            if(location):
                pass
            # methodCall
            # TODO
            method = ctx.methodCall()
            if(method):
                pass
            # literal
            literal = ctx.literal()
            if(literal):
                if(literal.int_literal()):
                    retrunArray.append('int')
                elif(literal.char_literal()):
                    retrunArray.append('char')
                elif(literal.bool_literal()):
                    retrunArray.append('boolean')

    def exitExpression(self, ctx: decafParser.ExpressionContext):
        global procesandoReturn
        global retrunArray
        global funcionTemp

        if(len(retrunArray) > 2):
            funcionTemp.procesarReturn(retrunArray)
            retrunArray = []

    def enterOp(self, ctx: decafParser.OpContext):
        global procesandoReturn
        global retrunArray

        if (procesandoReturn):
            # arith_op
            if(ctx.arith_op()):
                retrunArray.append('intOp')

            # rel_op
            if(ctx.rel_op()):
                retrunArray.append('relOp')

            # eq_op
            if(ctx.eq_op()):
                retrunArray.append('eqOp')

            # cond_op
            if(ctx.cond_op()):
                retrunArray.append('boolOp')

    def exitReturnStatement(self, ctx: decafParser.ReturnStatementContext):
        global procesandoReturn
        global retrunArray
        global funcionTemp
        print(f'''
        -----
        exitReturnStatement
        -----
        retrunArray {retrunArray}
        ''')

        if(len(retrunArray) >= 2):
            funcionTemp.procesarReturn(retrunArray)
            procesandoReturn = False
            retrunArray = []
            funcionTemp.agregarReturn()
        elif(len(retrunArray) == 1):
            funcionTemp.agregarReturn(retrunArray.pop())
        else:
            funcionTemp.agregarReturn()

    def exitMethodDeclaration(self, ctx: decafParser.MethodDeclarationContext):
        global funcionTemp
        global funcionNombreTemp
        global procesandoReturn
        global retrunArray
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
        procesandoReturn = False
        retrunArray = []

    def enterVarDeclaration(self, ctx: decafParser.VarDeclarationContext):
        # revisar si es array
        if(len(ctx.children) == 6):
            # es la declaracion de un array
            long = int(ctx.children[3].getText())
            if(long < 0):
                print(
                    f"Error en declaracion de array linea {ctx.start.line}: la dimension debe ser positiva")
            else:
                nombre = ctx.id_tok().getText()
                tipo = ctx.varType().getText()
                declaracionTemp = self.agregarVariableATabla(
                    nombre, Variable(tipo, long=long))
                if(declaracionTemp):
                    print(
                        f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp}")

        else:
            # es la declaracion de una variable
            nombre = ctx.id_tok().getText()
            tipo = ctx.varType().getText()
            declaracionTemp = self.agregarVariableATabla(
                nombre, Variable(tipo))
            if(declaracionTemp):
                print(
                    f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp}")

    def enterStart(self, ctx: decafParser.StartContext):
        # Se crea el ambito global
        pilaVariable.append({})
        pilaFuncion.append({})
        pilaEstructura.append({})


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
