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
        self.tablaVar = []
        self.tablaFunc = []
        self.tablaEstruct = []

    def agregarVariableATabla(self, nombre, variable):
        if(nombre in pilaVariable[-1].keys()):
            return 'Esta variable ya existe'
        else:
            pilaVariable[-1][nombre] = variable

        print('\n### Pila Variables')
        print(pilaVariable)

    def agregarFuncionATabla(self, nombre, funcion):
        if(nombre in pilaFuncion[-1].keys()):
            return 'Esta funcion ya existe'
        else:
            pilaFuncion[-1][nombre] = funcion

        print('\n### Pila funciones')
        print(pilaFuncion)

    def procesarLiteral(self, literal):
        '''
        literal
        int_literal
        char_literal
        bool_literal
        '''

        if (literal.int_literal()):
            # int_literal
            return 'int'
            print(f"literal int {literal.int_literal().getText()}")

        elif (literal.char_literal()):
            # int_literal
            return 'char'
            print(f"literal char {literal.char_literal().getText()}")

        elif (literal.bool_literal()):
            # int_literal
            return 'boolean'
            print(f"literal bool {literal.bool_literal().getText()}")

    def procesarRetorno(self, returnStatement):

        if (returnStatement.expression().literal()):
            # es literal
            return self.procesarLiteral(returnStatement.expression().literal())

        return 1

    def procesarParametros(self, parametros):
        parametrosList = []

        if (parametros[0].getText() == 'void' and len(parametros) == 1):
            return parametrosList

        for i in parametros:
            nombre = i.id_tok().getText()
            tipo = i.parameterType().getText()
            parametrosList.append(Variable(nombre, tipo))

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

        funcionTemp = Funcion(tipo, parametros)
        funcionNombreTemp = nombre

    def enterReturnStatement(self, ctx: decafParser.ReturnStatementContext):
        print('return')
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

        print(retrunArray)
        print(len(retrunArray))

        if(len(retrunArray) > 2):
            funcionTemp.procesarReturn(retrunArray)
            retrunArray = []

    def enterOp(self, ctx: decafParser.OpContext):
        print('Op')
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

        if(len(retrunArray) > 2):
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
        funcionTemp.validar()
        if (funcionTemp.err):
            # si hay error en definicion de funcion
            print(
                f"Error en declaracion de funcion linea {ctx.start.line}: {funcionTemp.err}")
            funcionNombreTemp = None
            funcionTemp = None
        else:
            # si no hay error se agrega a tabla
            self.agregarFuncionATabla(funcionNombreTemp, funcionTemp)
            funcionNombreTemp = None
            funcionTemp = None

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


def traverse(tree, rule_names, indent=0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        #print("{0}T='{1}'".format("  " * indent, tree.getText()))
        pass
    else:
        #print("{0}R='{1}'".format("  " * indent,rule_names[tree.getRuleIndex()]))

        if (rule_names[tree.getRuleIndex()] == 'methodDeclaration'):
            print('funct')
            #procesarFuncion(tree.children, rule_names)
        if (tree.children != None):
            for child in tree.children:
                traverse(child, rule_names, indent + 1)


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

    #traverse(tree, parser.ruleNames)

    # print(tree.getText())
    # print(tree.getRuleIndex())
    # print(parser.ruleNames)

    # print(tree.getChild(1))

    #print(tree.getToken(3, 0))
    # print(tree.getTokens(3))

    print()


if __name__ == '__main__':
    main()
