from typing import List
from antlr4 import *
from decafLexer import decafLexer
from decafVisitor import decafVisitor
from decafParser import decafParser


class EvalVisitor(decafVisitor):
    def visitar(self, tree):
        if(isinstance(tree, list)):
            resultados = []
            for i in tree:
                resultados.append(self.visit(i))
            return resultados
        else:
            return self.visit(tree)

    def visitProgramStart(self, ctx: decafParser.ProgramStartContext):
        return self.visitar(ctx.declaration())

    def visitMethodDec(self, ctx: decafParser.MethodDecContext):
        return ctx.id_tok().getText()


def main():
    data = open('../decafPrograms/hello_world.txt').read()
    lexer = decafLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = decafParser(stream)
    tree = parser.start()
    answer = EvalVisitor().visit(tree)
    print(answer)


if __name__ == '__main__':
    main()
