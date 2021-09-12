from antlr4 import *
from decafLexer import decafLexer
from decafVisitor import decafVisitor
from decafParser import decafParser
import copy
import sys


class DecafPrinter(decafVisitor):
    def __init__(self) -> None:
        super().__init__()

    def visitProgramStart(self, ctx: decafParser.ProgramStartContext):
        return self.visit(ctx.declaration())


def main():
    data = open('./decafPrograms/hello_world.txt').read()

    lexer = decafLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = decafParser(stream)
    parser.buildParseTrees = True
    tree = parser.start()

    visitor = DecafPrinter()
    tree.accept(visitor)
    ast = DecafPrinter().visit(tree)
    print(ast)


if __name__ == '__main__':
    main()
