# Generated from decaf.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .decafParser import decafParser
else:
    from decafParser import decafParser

# This class defines a complete listener for a parse tree produced by decafParser.
class decafListener(ParseTreeListener):

    # Enter a parse tree produced by decafParser#programStart.
    def enterProgramStart(self, ctx:decafParser.ProgramStartContext):
        pass

    # Exit a parse tree produced by decafParser#programStart.
    def exitProgramStart(self, ctx:decafParser.ProgramStartContext):
        pass


    # Enter a parse tree produced by decafParser#declarationStruct.
    def enterDeclarationStruct(self, ctx:decafParser.DeclarationStructContext):
        pass

    # Exit a parse tree produced by decafParser#declarationStruct.
    def exitDeclarationStruct(self, ctx:decafParser.DeclarationStructContext):
        pass


    # Enter a parse tree produced by decafParser#declarationVar.
    def enterDeclarationVar(self, ctx:decafParser.DeclarationVarContext):
        pass

    # Exit a parse tree produced by decafParser#declarationVar.
    def exitDeclarationVar(self, ctx:decafParser.DeclarationVarContext):
        pass


    # Enter a parse tree produced by decafParser#declarationMethod.
    def enterDeclarationMethod(self, ctx:decafParser.DeclarationMethodContext):
        pass

    # Exit a parse tree produced by decafParser#declarationMethod.
    def exitDeclarationMethod(self, ctx:decafParser.DeclarationMethodContext):
        pass


    # Enter a parse tree produced by decafParser#varDec.
    def enterVarDec(self, ctx:decafParser.VarDecContext):
        pass

    # Exit a parse tree produced by decafParser#varDec.
    def exitVarDec(self, ctx:decafParser.VarDecContext):
        pass


    # Enter a parse tree produced by decafParser#arrayDec.
    def enterArrayDec(self, ctx:decafParser.ArrayDecContext):
        pass

    # Exit a parse tree produced by decafParser#arrayDec.
    def exitArrayDec(self, ctx:decafParser.ArrayDecContext):
        pass


    # Enter a parse tree produced by decafParser#structDec.
    def enterStructDec(self, ctx:decafParser.StructDecContext):
        pass

    # Exit a parse tree produced by decafParser#structDec.
    def exitStructDec(self, ctx:decafParser.StructDecContext):
        pass


    # Enter a parse tree produced by decafParser#intVarType.
    def enterIntVarType(self, ctx:decafParser.IntVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#intVarType.
    def exitIntVarType(self, ctx:decafParser.IntVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#charVarType.
    def enterCharVarType(self, ctx:decafParser.CharVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#charVarType.
    def exitCharVarType(self, ctx:decafParser.CharVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#booleanVarType.
    def enterBooleanVarType(self, ctx:decafParser.BooleanVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#booleanVarType.
    def exitBooleanVarType(self, ctx:decafParser.BooleanVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#structVarType.
    def enterStructVarType(self, ctx:decafParser.StructVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#structVarType.
    def exitStructVarType(self, ctx:decafParser.StructVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#structDecVarType.
    def enterStructDecVarType(self, ctx:decafParser.StructDecVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#structDecVarType.
    def exitStructDecVarType(self, ctx:decafParser.StructDecVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#voidVarType.
    def enterVoidVarType(self, ctx:decafParser.VoidVarTypeContext):
        pass

    # Exit a parse tree produced by decafParser#voidVarType.
    def exitVoidVarType(self, ctx:decafParser.VoidVarTypeContext):
        pass


    # Enter a parse tree produced by decafParser#methodDec.
    def enterMethodDec(self, ctx:decafParser.MethodDecContext):
        pass

    # Exit a parse tree produced by decafParser#methodDec.
    def exitMethodDec(self, ctx:decafParser.MethodDecContext):
        pass


    # Enter a parse tree produced by decafParser#intMethod.
    def enterIntMethod(self, ctx:decafParser.IntMethodContext):
        pass

    # Exit a parse tree produced by decafParser#intMethod.
    def exitIntMethod(self, ctx:decafParser.IntMethodContext):
        pass


    # Enter a parse tree produced by decafParser#charMethod.
    def enterCharMethod(self, ctx:decafParser.CharMethodContext):
        pass

    # Exit a parse tree produced by decafParser#charMethod.
    def exitCharMethod(self, ctx:decafParser.CharMethodContext):
        pass


    # Enter a parse tree produced by decafParser#booleanMethod.
    def enterBooleanMethod(self, ctx:decafParser.BooleanMethodContext):
        pass

    # Exit a parse tree produced by decafParser#booleanMethod.
    def exitBooleanMethod(self, ctx:decafParser.BooleanMethodContext):
        pass


    # Enter a parse tree produced by decafParser#voidMethod.
    def enterVoidMethod(self, ctx:decafParser.VoidMethodContext):
        pass

    # Exit a parse tree produced by decafParser#voidMethod.
    def exitVoidMethod(self, ctx:decafParser.VoidMethodContext):
        pass


    # Enter a parse tree produced by decafParser#idParam.
    def enterIdParam(self, ctx:decafParser.IdParamContext):
        pass

    # Exit a parse tree produced by decafParser#idParam.
    def exitIdParam(self, ctx:decafParser.IdParamContext):
        pass


    # Enter a parse tree produced by decafParser#arrayParam.
    def enterArrayParam(self, ctx:decafParser.ArrayParamContext):
        pass

    # Exit a parse tree produced by decafParser#arrayParam.
    def exitArrayParam(self, ctx:decafParser.ArrayParamContext):
        pass


    # Enter a parse tree produced by decafParser#voidParam.
    def enterVoidParam(self, ctx:decafParser.VoidParamContext):
        pass

    # Exit a parse tree produced by decafParser#voidParam.
    def exitVoidParam(self, ctx:decafParser.VoidParamContext):
        pass


    # Enter a parse tree produced by decafParser#intParam.
    def enterIntParam(self, ctx:decafParser.IntParamContext):
        pass

    # Exit a parse tree produced by decafParser#intParam.
    def exitIntParam(self, ctx:decafParser.IntParamContext):
        pass


    # Enter a parse tree produced by decafParser#charParam.
    def enterCharParam(self, ctx:decafParser.CharParamContext):
        pass

    # Exit a parse tree produced by decafParser#charParam.
    def exitCharParam(self, ctx:decafParser.CharParamContext):
        pass


    # Enter a parse tree produced by decafParser#booleanParam.
    def enterBooleanParam(self, ctx:decafParser.BooleanParamContext):
        pass

    # Exit a parse tree produced by decafParser#booleanParam.
    def exitBooleanParam(self, ctx:decafParser.BooleanParamContext):
        pass


    # Enter a parse tree produced by decafParser#blockDec.
    def enterBlockDec(self, ctx:decafParser.BlockDecContext):
        pass

    # Exit a parse tree produced by decafParser#blockDec.
    def exitBlockDec(self, ctx:decafParser.BlockDecContext):
        pass


    # Enter a parse tree produced by decafParser#ifStmt.
    def enterIfStmt(self, ctx:decafParser.IfStmtContext):
        pass

    # Exit a parse tree produced by decafParser#ifStmt.
    def exitIfStmt(self, ctx:decafParser.IfStmtContext):
        pass


    # Enter a parse tree produced by decafParser#whileStmt.
    def enterWhileStmt(self, ctx:decafParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by decafParser#whileStmt.
    def exitWhileStmt(self, ctx:decafParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by decafParser#returnStmt.
    def enterReturnStmt(self, ctx:decafParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by decafParser#returnStmt.
    def exitReturnStmt(self, ctx:decafParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by decafParser#methodStmt.
    def enterMethodStmt(self, ctx:decafParser.MethodStmtContext):
        pass

    # Exit a parse tree produced by decafParser#methodStmt.
    def exitMethodStmt(self, ctx:decafParser.MethodStmtContext):
        pass


    # Enter a parse tree produced by decafParser#blockStmt.
    def enterBlockStmt(self, ctx:decafParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by decafParser#blockStmt.
    def exitBlockStmt(self, ctx:decafParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by decafParser#assignmentStmt.
    def enterAssignmentStmt(self, ctx:decafParser.AssignmentStmtContext):
        pass

    # Exit a parse tree produced by decafParser#assignmentStmt.
    def exitAssignmentStmt(self, ctx:decafParser.AssignmentStmtContext):
        pass


    # Enter a parse tree produced by decafParser#expressionStmt.
    def enterExpressionStmt(self, ctx:decafParser.ExpressionStmtContext):
        pass

    # Exit a parse tree produced by decafParser#expressionStmt.
    def exitExpressionStmt(self, ctx:decafParser.ExpressionStmtContext):
        pass


    # Enter a parse tree produced by decafParser#idLocation.
    def enterIdLocation(self, ctx:decafParser.IdLocationContext):
        pass

    # Exit a parse tree produced by decafParser#idLocation.
    def exitIdLocation(self, ctx:decafParser.IdLocationContext):
        pass


    # Enter a parse tree produced by decafParser#idLocationDot.
    def enterIdLocationDot(self, ctx:decafParser.IdLocationDotContext):
        pass

    # Exit a parse tree produced by decafParser#idLocationDot.
    def exitIdLocationDot(self, ctx:decafParser.IdLocationDotContext):
        pass


    # Enter a parse tree produced by decafParser#arrayLocation.
    def enterArrayLocation(self, ctx:decafParser.ArrayLocationContext):
        pass

    # Exit a parse tree produced by decafParser#arrayLocation.
    def exitArrayLocation(self, ctx:decafParser.ArrayLocationContext):
        pass


    # Enter a parse tree produced by decafParser#arrayLocationDot.
    def enterArrayLocationDot(self, ctx:decafParser.ArrayLocationDotContext):
        pass

    # Exit a parse tree produced by decafParser#arrayLocationDot.
    def exitArrayLocationDot(self, ctx:decafParser.ArrayLocationDotContext):
        pass


    # Enter a parse tree produced by decafParser#methodCallExpr.
    def enterMethodCallExpr(self, ctx:decafParser.MethodCallExprContext):
        pass

    # Exit a parse tree produced by decafParser#methodCallExpr.
    def exitMethodCallExpr(self, ctx:decafParser.MethodCallExprContext):
        pass


    # Enter a parse tree produced by decafParser#parExpr.
    def enterParExpr(self, ctx:decafParser.ParExprContext):
        pass

    # Exit a parse tree produced by decafParser#parExpr.
    def exitParExpr(self, ctx:decafParser.ParExprContext):
        pass


    # Enter a parse tree produced by decafParser#eqExpr.
    def enterEqExpr(self, ctx:decafParser.EqExprContext):
        pass

    # Exit a parse tree produced by decafParser#eqExpr.
    def exitEqExpr(self, ctx:decafParser.EqExprContext):
        pass


    # Enter a parse tree produced by decafParser#notExpr.
    def enterNotExpr(self, ctx:decafParser.NotExprContext):
        pass

    # Exit a parse tree produced by decafParser#notExpr.
    def exitNotExpr(self, ctx:decafParser.NotExprContext):
        pass


    # Enter a parse tree produced by decafParser#secondArithExpr.
    def enterSecondArithExpr(self, ctx:decafParser.SecondArithExprContext):
        pass

    # Exit a parse tree produced by decafParser#secondArithExpr.
    def exitSecondArithExpr(self, ctx:decafParser.SecondArithExprContext):
        pass


    # Enter a parse tree produced by decafParser#locationExpr.
    def enterLocationExpr(self, ctx:decafParser.LocationExprContext):
        pass

    # Exit a parse tree produced by decafParser#locationExpr.
    def exitLocationExpr(self, ctx:decafParser.LocationExprContext):
        pass


    # Enter a parse tree produced by decafParser#literalExpr.
    def enterLiteralExpr(self, ctx:decafParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by decafParser#literalExpr.
    def exitLiteralExpr(self, ctx:decafParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by decafParser#negativeExpr.
    def enterNegativeExpr(self, ctx:decafParser.NegativeExprContext):
        pass

    # Exit a parse tree produced by decafParser#negativeExpr.
    def exitNegativeExpr(self, ctx:decafParser.NegativeExprContext):
        pass


    # Enter a parse tree produced by decafParser#condExpr.
    def enterCondExpr(self, ctx:decafParser.CondExprContext):
        pass

    # Exit a parse tree produced by decafParser#condExpr.
    def exitCondExpr(self, ctx:decafParser.CondExprContext):
        pass


    # Enter a parse tree produced by decafParser#relExpr.
    def enterRelExpr(self, ctx:decafParser.RelExprContext):
        pass

    # Exit a parse tree produced by decafParser#relExpr.
    def exitRelExpr(self, ctx:decafParser.RelExprContext):
        pass


    # Enter a parse tree produced by decafParser#firstArithExpr.
    def enterFirstArithExpr(self, ctx:decafParser.FirstArithExprContext):
        pass

    # Exit a parse tree produced by decafParser#firstArithExpr.
    def exitFirstArithExpr(self, ctx:decafParser.FirstArithExprContext):
        pass


    # Enter a parse tree produced by decafParser#methodCallDec.
    def enterMethodCallDec(self, ctx:decafParser.MethodCallDecContext):
        pass

    # Exit a parse tree produced by decafParser#methodCallDec.
    def exitMethodCallDec(self, ctx:decafParser.MethodCallDecContext):
        pass


    # Enter a parse tree produced by decafParser#argDec.
    def enterArgDec(self, ctx:decafParser.ArgDecContext):
        pass

    # Exit a parse tree produced by decafParser#argDec.
    def exitArgDec(self, ctx:decafParser.ArgDecContext):
        pass


    # Enter a parse tree produced by decafParser#intLiteral.
    def enterIntLiteral(self, ctx:decafParser.IntLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#intLiteral.
    def exitIntLiteral(self, ctx:decafParser.IntLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#charLiteral.
    def enterCharLiteral(self, ctx:decafParser.CharLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#charLiteral.
    def exitCharLiteral(self, ctx:decafParser.CharLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#boolLiteral.
    def enterBoolLiteral(self, ctx:decafParser.BoolLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#boolLiteral.
    def exitBoolLiteral(self, ctx:decafParser.BoolLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#numLiteral.
    def enterNumLiteral(self, ctx:decafParser.NumLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#numLiteral.
    def exitNumLiteral(self, ctx:decafParser.NumLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#trueLiteral.
    def enterTrueLiteral(self, ctx:decafParser.TrueLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#trueLiteral.
    def exitTrueLiteral(self, ctx:decafParser.TrueLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#falseLiteral.
    def enterFalseLiteral(self, ctx:decafParser.FalseLiteralContext):
        pass

    # Exit a parse tree produced by decafParser#falseLiteral.
    def exitFalseLiteral(self, ctx:decafParser.FalseLiteralContext):
        pass


    # Enter a parse tree produced by decafParser#idDec.
    def enterIdDec(self, ctx:decafParser.IdDecContext):
        pass

    # Exit a parse tree produced by decafParser#idDec.
    def exitIdDec(self, ctx:decafParser.IdDecContext):
        pass


    # Enter a parse tree produced by decafParser#numDec.
    def enterNumDec(self, ctx:decafParser.NumDecContext):
        pass

    # Exit a parse tree produced by decafParser#numDec.
    def exitNumDec(self, ctx:decafParser.NumDecContext):
        pass



del decafParser