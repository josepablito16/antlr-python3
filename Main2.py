from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from decafLexer import decafLexer
from decafListener import decafListener
from decafParser import decafParser
from Variable import *
from Funcion import *
import sys


def procesarRetorno(tree, rule_names):
    '''
        si el penultimo hijo es de tipo returnStatement
        entonces tiene valor de retorno, sino la func
        no retorna nada 
    '''
    if(rule_names[tree[-2].getRuleIndex()] == 'returnStatement'):
        tipoRetorno = rule_names[tree[-2].children[1]
                                 .children[0].children[0].getRuleIndex()]
        retorno = tree[-2].children[1].children[0].getText()

        return tipoRetorno, retorno
    else:
        return None, None


def procesarParametro(tree):
    tipo = tree[0].getText()
    nombre = tree[1].getText()

    return Variable(nombre, tipo)


def procesarFuncion(tree, rule_names):

    if(len(tree) > 5):
        '''
        > de 5, tiene parametros
        methodType 0
        id_tok 1
        ( 2
        parameter 3-len()-2
        ) -2
        block -1
        '''
        tipo = tree[0].getText()
        nombre = tree[1].getText()
        tipoRetorno, retorno = procesarRetorno(tree[-1].children, rule_names)

        '''
        Se recorren los hijos que corresponden a los parametros,
        saltando los hijos ,
        '''
        parametros = []
        for i in range(3, len(tree)-2, 2):
            parametros.append(procesarParametro(tree[i].children))

        """
        print(f'''
        tipo = {tipo}
        nombre = {nombre}
        parametros = {parametros}
        tipoRetorno = {tipoRetorno}
        retorno = {retorno}''')
        """

        func = None
        if tipoRetorno != None:
            func = Funcion(tipo, parametros, Variable(retorno, tipoRetorno))
        else:
            func = Funcion(tipo, parametros)

        func.validar()
        print(func.err)
        print(func)

    else:
        '''
        5 sin parametros

        methodType 0
        id_tok 1
        ( 2
        ) 3
        block 4
        '''
        tipo = tree[0].getText()
        nombre = tree[1].getText()
        tipoRetorno, retorno = procesarRetorno(tree[4].children, rule_names)
        """
        print(f'''
        tipo = {tipo}
        nombre = {nombre}
        tipoRetorno = {tipoRetorno}
        retorno = {retorno}''')
        """

        func = None
        if tipoRetorno != None:
            func = Funcion(tipo, [], Variable(retorno, tipoRetorno))
        else:
            func = Funcion(tipo)

        func.validar()
        print(func.err)
        print(func)


class DecafPrinter(decafListener):
    def __init__(self) -> None:
        super().__init__()

    def procesarLiteral(self, literal):
        '''
        literal
        int_literal
        char_literal
        bool_literal
        '''

        if (literal.int_literal()):
            # int_literal
            return Variable('Test', 'int')
            print(f"literal int {literal.int_literal().getText()}")

        elif (literal.char_literal()):
            # int_literal
            return Variable('Test', 'char')
            print(f"literal char {literal.char_literal().getText()}")

        elif (literal.bool_literal()):
            # int_literal
            return Variable('Test', 'boolean')
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
            func = Funcion(tipo, parametros, retorno)
        else:
            func = Funcion(tipo, parametros)

        func.validar()

        if (func.err != None):
            print(f'Error en funcion linea {ctx.start.line}: {func.err}')
        print(f'''
        tipo = {tipo}
        nombre = {nombre}
        parametros = {parametros}
        retorno = {retorno}''')


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
            procesarFuncion(tree.children, rule_names)
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
