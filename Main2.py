from antlr4 import *
from antlr4.tree.Trees import TerminalNode
from decafLexer import decafLexer
from decafListener import decafListener
from decafParser import decafParser
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


def procesarFuncion(tree, rule_names):

    # > de 5, tiene parametros
    '''
    methodType 0
    id_tok 1
    ( 2
    parameter 3-len()-2
    ) -2
    block -1
    '''
    if(len(tree) > 5):
        pass
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
        print(f'''
        tipo = {tipo}
        nombre = {nombre}
        tipoRetorno = {tipoRetorno}
        retorno = {retorno}''')


class KeyPrinter(decafListener):
    def exitKey(self, ctx):
        print("Hello: %s" % ctx.ID())


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

    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    traverse(tree, parser.ruleNames)

    # print(tree.getText())
    # print(tree.getRuleIndex())
    # print(parser.ruleNames)

    # print(tree.getChild(1))

    #print(tree.getToken(3, 0))
    # print(tree.getTokens(3))

    print()


if __name__ == '__main__':
    main()
