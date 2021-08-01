# Generated from decaf.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .decafParser import decafParser
else:
    from decafParser import decafParser

# This class defines a complete listener for a parse tree produced by decafParser.
class decafListener(ParseTreeListener):

    # Enter a parse tree produced by decafParser#start.
    def enterStart(self, ctx:decafParser.StartContext):
        pass

    # Exit a parse tree produced by decafParser#start.
    def exitStart(self, ctx:decafParser.StartContext):
        pass


    # Enter a parse tree produced by decafParser#id_tok.
    def enterId_tok(self, ctx:decafParser.Id_tokContext):
        pass

    # Exit a parse tree produced by decafParser#id_tok.
    def exitId_tok(self, ctx:decafParser.Id_tokContext):
        pass


    # Enter a parse tree produced by decafParser#declaration.
    def enterDeclaration(self, ctx:decafParser.DeclarationContext):
        pass

    # Exit a parse tree produced by decafParser#declaration.
    def exitDeclaration(self, ctx:decafParser.DeclarationContext):
        pass


    # Enter a parse tree produced by decafParser#varDeclaration.
    def enterVarDeclaration(self, ctx:decafParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by decafParser#varDeclaration.
    def exitVarDeclaration(self, ctx:decafParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by decafParser#structDeclaration.
    def enterStructDeclaration(self, ctx:decafParser.StructDeclarationContext):
        pass

    # Exit a parse tree produced by decafParser#structDeclaration.
    def exitStructDeclaration(self, ctx:decafParser.StructDeclarationContext):
        pass


    # Enter a parse tree produced by decafParser#varType.
    def enterVarType(self, ctx:decafParser.VarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#varType.
    def exitVarType(self, ctx:decafParser.VarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:decafParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by decafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:decafParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by decafParser#methodType.
    def enterMethodType(self, ctx:decafParser.MethodTypeContext):
        pass

    # Exit a parse tree produced by decafParser#methodType.
    def exitMethodType(self, ctx:decafParser.MethodTypeContext):
        pass


    # Enter a parse tree produced by decafParser#parameter.
    def enterParameter(self, ctx:decafParser.ParameterContext):
        pass

    # Exit a parse tree produced by decafParser#parameter.
    def exitParameter(self, ctx:decafParser.ParameterContext):
        pass


    # Enter a parse tree produced by decafParser#parameterType.
    def enterParameterType(self, ctx:decafParser.ParameterTypeContext):
        pass

    # Exit a parse tree produced by decafParser#parameterType.
    def exitParameterType(self, ctx:decafParser.ParameterTypeContext):
        pass


    # Enter a parse tree produced by decafParser#block.
    def enterBlock(self, ctx:decafParser.BlockContext):
        pass

    # Exit a parse tree produced by decafParser#block.
    def exitBlock(self, ctx:decafParser.BlockContext):
        pass


    # Enter a parse tree produced by decafParser#statement.
    def enterStatement(self, ctx:decafParser.StatementContext):
        pass

    # Exit a parse tree produced by decafParser#statement.
    def exitStatement(self, ctx:decafParser.StatementContext):
        pass


    # Enter a parse tree produced by decafParser#location.
    def enterLocation(self, ctx:decafParser.LocationContext):
        pass

    # Exit a parse tree produced by decafParser#location.
    def exitLocation(self, ctx:decafParser.LocationContext):
        pass


    # Enter a parse tree produced by decafParser#expression.
    def enterExpression(self, ctx:decafParser.ExpressionContext):
        pass

    # Exit a parse tree produced by decafParser#expression.
    def exitExpression(self, ctx:decafParser.ExpressionContext):
        pass


    # Enter a parse tree produced by decafParser#methodCall.
    def enterMethodCall(self, ctx:decafParser.MethodCallContext):
        pass

    # Exit a parse tree produced by decafParser#methodCall.
    def exitMethodCall(self, ctx:decafParser.MethodCallContext):
        pass


    # Enter a parse tree produced by decafParser#arg.
    def enterArg(self, ctx:decafParser.ArgContext):
        pass

    # Exit a parse tree produced by decafParser#arg.
    def exitArg(self, ctx:decafParser.ArgContext):
        pass


    # Enter a parse tree produced by decafParser#op.
    def enterOp(self, ctx:decafParser.OpContext):
        pass

    # Exit a parse tree produced by decafParser#op.
    def exitOp(self, ctx:decafParser.OpContext):
        pass


    # Enter a parse tree produced by decafParser#arith_op.
    def enterArith_op(self, ctx:decafParser.Arith_opContext):
        pass

    # Exit a parse tree produced by decafParser#arith_op.
    def exitArith_op(self, ctx:decafParser.Arith_opContext):
        pass


    # Enter a parse tree produced by decafParser#rel_op.
    def enterRel_op(self, ctx:decafParser.Rel_opContext):
        pass

    # Exit a parse tree produced by decafParser#rel_op.
    def exitRel_op(self, ctx:decafParser.Rel_opContext):
        pass


    # Enter a parse tree produced by decafParser#eq_op.
    def enterEq_op(self, ctx:decafParser.Eq_opContext):
        pass

    # Exit a parse tree produced by decafParser#eq_op.
    def exitEq_op(self, ctx:decafParser.Eq_opContext):
        pass


    # Enter a parse tree produced by decafParser#cond_op.
    def enterCond_op(self, ctx:decafParser.Cond_opContext):
        pass

    # Exit a parse tree produced by decafParser#cond_op.
    def exitCond_op(self, ctx:decafParser.Cond_opContext):
        pass


    # Enter a parse tree produced by decafParser#literal.
    def enterLiteral(self, ctx:decafParser.LiteralContext):
        pass

    # Exit a parse tree produced by decafParser#literal.
    def exitLiteral(self, ctx:decafParser.LiteralContext):
        pass


    # Enter a parse tree produced by decafParser#int_literal.
    def enterInt_literal(self, ctx:decafParser.Int_literalContext):
        pass

    # Exit a parse tree produced by decafParser#int_literal.
    def exitInt_literal(self, ctx:decafParser.Int_literalContext):
        pass


    # Enter a parse tree produced by decafParser#char_literal.
    def enterChar_literal(self, ctx:decafParser.Char_literalContext):
        pass

    # Exit a parse tree produced by decafParser#char_literal.
    def exitChar_literal(self, ctx:decafParser.Char_literalContext):
        pass


    # Enter a parse tree produced by decafParser#bool_literal.
    def enterBool_literal(self, ctx:decafParser.Bool_literalContext):
        pass

    # Exit a parse tree produced by decafParser#bool_literal.
    def exitBool_literal(self, ctx:decafParser.Bool_literalContext):
        pass



del decafParser