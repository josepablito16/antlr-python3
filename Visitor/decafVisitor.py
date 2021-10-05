# Generated from decaf.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .decafParser import decafParser
else:
    from decafParser import decafParser

# This class defines a complete generic visitor for a parse tree produced by decafParser.

class decafVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by decafParser#programStart.
    def visitProgramStart(self, ctx:decafParser.ProgramStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#declarationStruct.
    def visitDeclarationStruct(self, ctx:decafParser.DeclarationStructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#declarationVar.
    def visitDeclarationVar(self, ctx:decafParser.DeclarationVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#declarationMethod.
    def visitDeclarationMethod(self, ctx:decafParser.DeclarationMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#varDec.
    def visitVarDec(self, ctx:decafParser.VarDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#arrayDec.
    def visitArrayDec(self, ctx:decafParser.ArrayDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#structDec.
    def visitStructDec(self, ctx:decafParser.StructDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#intVarType.
    def visitIntVarType(self, ctx:decafParser.IntVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#charVarType.
    def visitCharVarType(self, ctx:decafParser.CharVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#booleanVarType.
    def visitBooleanVarType(self, ctx:decafParser.BooleanVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#structVarType.
    def visitStructVarType(self, ctx:decafParser.StructVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#structDecVarType.
    def visitStructDecVarType(self, ctx:decafParser.StructDecVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#voidVarType.
    def visitVoidVarType(self, ctx:decafParser.VoidVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#methodDec.
    def visitMethodDec(self, ctx:decafParser.MethodDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#intMethod.
    def visitIntMethod(self, ctx:decafParser.IntMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#charMethod.
    def visitCharMethod(self, ctx:decafParser.CharMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#booleanMethod.
    def visitBooleanMethod(self, ctx:decafParser.BooleanMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#voidMethod.
    def visitVoidMethod(self, ctx:decafParser.VoidMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#idParam.
    def visitIdParam(self, ctx:decafParser.IdParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#arrayParam.
    def visitArrayParam(self, ctx:decafParser.ArrayParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#voidParam.
    def visitVoidParam(self, ctx:decafParser.VoidParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#intParam.
    def visitIntParam(self, ctx:decafParser.IntParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#charParam.
    def visitCharParam(self, ctx:decafParser.CharParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#booleanParam.
    def visitBooleanParam(self, ctx:decafParser.BooleanParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#blockDec.
    def visitBlockDec(self, ctx:decafParser.BlockDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#ifStmt.
    def visitIfStmt(self, ctx:decafParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#ifElseStmt.
    def visitIfElseStmt(self, ctx:decafParser.IfElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#whileStmt.
    def visitWhileStmt(self, ctx:decafParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#returnStmt.
    def visitReturnStmt(self, ctx:decafParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#methodStmt.
    def visitMethodStmt(self, ctx:decafParser.MethodStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#blockStmt.
    def visitBlockStmt(self, ctx:decafParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#assignmentStmt.
    def visitAssignmentStmt(self, ctx:decafParser.AssignmentStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#expressionStmt.
    def visitExpressionStmt(self, ctx:decafParser.ExpressionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#idLocation.
    def visitIdLocation(self, ctx:decafParser.IdLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#idLocationDot.
    def visitIdLocationDot(self, ctx:decafParser.IdLocationDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#arrayLocation.
    def visitArrayLocation(self, ctx:decafParser.ArrayLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#arrayLocationDot.
    def visitArrayLocationDot(self, ctx:decafParser.ArrayLocationDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#methodCallExpr.
    def visitMethodCallExpr(self, ctx:decafParser.MethodCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#parExpr.
    def visitParExpr(self, ctx:decafParser.ParExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#eqExpr.
    def visitEqExpr(self, ctx:decafParser.EqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#notExpr.
    def visitNotExpr(self, ctx:decafParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#secondArithExpr.
    def visitSecondArithExpr(self, ctx:decafParser.SecondArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#locationExpr.
    def visitLocationExpr(self, ctx:decafParser.LocationExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#literalExpr.
    def visitLiteralExpr(self, ctx:decafParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#negativeExpr.
    def visitNegativeExpr(self, ctx:decafParser.NegativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#condExpr.
    def visitCondExpr(self, ctx:decafParser.CondExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#relExpr.
    def visitRelExpr(self, ctx:decafParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#firstArithExpr.
    def visitFirstArithExpr(self, ctx:decafParser.FirstArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#methodCallDec.
    def visitMethodCallDec(self, ctx:decafParser.MethodCallDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#argDec.
    def visitArgDec(self, ctx:decafParser.ArgDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#intLiteral.
    def visitIntLiteral(self, ctx:decafParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#charLiteral.
    def visitCharLiteral(self, ctx:decafParser.CharLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#boolLiteral.
    def visitBoolLiteral(self, ctx:decafParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#numLiteral.
    def visitNumLiteral(self, ctx:decafParser.NumLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#trueLiteral.
    def visitTrueLiteral(self, ctx:decafParser.TrueLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#falseLiteral.
    def visitFalseLiteral(self, ctx:decafParser.FalseLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#idDec.
    def visitIdDec(self, ctx:decafParser.IdDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by decafParser#numDec.
    def visitNumDec(self, ctx:decafParser.NumDecContext):
        return self.visitChildren(ctx)



del decafParser