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


class DecafPrinter(decafListener):
    def __init__(self) -> None:
        super().__init__()
        self.tablaVar = []
        self.tablaFunc = []
        self.tablaEstruct = []

    def agregarVariableATabla(self, nombre, variable):

        if(nombre in pilaVariable[-1].keys()):
            print('Existe')
            return 'Esta variable ya existe'
        else:
            pilaVariable[-1][nombre] = variable

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

        tipo = ctx.methodType().getText()
        nombre = ctx.id_tok().getText()
        retorno = None
        parametros = []
        if(ctx.block().returnStatement()):
            # hay retorno
            print('Hay retorno')
            retorno = self.procesarRetorno(
                ctx.block().returnStatement())

        if(len(ctx.parameter()) > 0):
            # Hay parametros
            parametros = self.procesarParametros(ctx.parameter())

        func = None
        if (retorno != None):
            # la funcion no tiene retorno
            func = Funcion(tipo, parametros, [retorno])
        else:
            func = Funcion(tipo, parametros)

        func.validar()

        if (func.err != None):
            print(f'Error en funcion linea {ctx.start.line}: {func.err}')
        """
        print(f'''
        tipo = {tipo}
        nombre = {nombre}
        parametros = {parametros}
        retorno = {retorno}''')
        """

    def enterVarDeclaration(self, ctx: decafParser.VarDeclarationContext):
        # revisar si es array
        if(len(ctx.children) == 6):
            # es la declaracion de un array
            if(int(ctx.children[3].getText()) < 0):
                print(
                    f"Error en declaracion de array linea {ctx.start.line}: la dimension debe ser positiva")

        else:
            # es la declaracion de una variable
            nombre = ctx.id_tok().getText()
            tipo = ctx.varType().getText()
            declaracionTemp = self.agregarVariableATabla(
                nombre, Variable(tipo))
            if(declaracionTemp):
                print(
                    f"Error en declaracion de variable linea {ctx.start.line}: {declaracionTemp}")
            print(pilaVariable)

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
