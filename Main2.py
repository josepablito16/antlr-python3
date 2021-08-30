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

'''
Aqui se guardan los parametros de la funcion
para luego al entrar al ambito de la funcion
ingresar esas variables
'''
ambitoVariableTemp = {}


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

    def agregarVariableAmbitoTemp(self, nombre, variable):
        '''
        Funcion que valida si una variable ya existe en el ambito temporal
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        El ambito temporal se crea para registrar los parametros de una funcion, antes
        de ingresar al block donde se crea el verdadero ambito.

        Parametros
        - nombre: string con el nombre de la variable
        - variable: objeto Variable con la informacion de la variable a ingresar.
        '''
        if(nombre in ambitoVariableTemp.keys()):
            return f'La variable "{nombre}" ya existe dentro de los parametros de la funcion'
        else:
            ambitoVariableTemp[nombre] = variable

        print(f'''
                # Pila Variables [temp]
                {ambitoVariableTemp}
                ''')

    def agregarAmbitoTempATabla(self):
        '''
        Pasa el ambitoTemp al ambito de la funcion y limpia
        el ambitoTemp.
        No retorna nada
        '''
        global ambitoVariableTemp
        pilaVariable[-1].update(ambitoVariableTemp)
        ambitoVariableTemp = {}

        print(f'''
                # Pila Variables
                {pilaVariable}
                ''')

    def validarReglaMain(self):
        try:
            if not(len(pilaFuncion[-1]['main'].argumentosTipos) == 0):
                return 'La funcion main contiene parametros'
        except:
            # no existe main
            return 'Programa sin funcion main'

    def agregarAmbito(self):
        pilaVariable.append({})
        pilaEstructura.append({})

    def quitarAmbito(self):
        pilaVariable.pop()
        pilaEstructura.pop()

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
        Funcion para procesar parametros, valida si tiene de parametro void
        no puede ir acompañado de mas tipos.

        Parametros
        - parametros: lista de nodos tipo parameter
        '''
        parametrosList = []

        # revisa si contiene de parametros void, no puede ir acompañado de más tipos
        if (parametros[0].getText() == 'void'):
            if (len(parametros) == 1):
                return parametrosList
            else:
                return 'parametro void no puede ir acompañado de mas parametros'

        for i in parametros:
            nombre = i.id_tok().getText()
            tipo = i.parameterType().getText()

            # Se agregan parametros a la tabla del ambito de esta funcion
            declaracionTemp = self.agregarVariableAmbitoTemp(
                nombre, Variable(tipo))
            if (declaracionTemp):
                return declaracionTemp

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
            if(long <= 0):
                print(
                    f"Error en declaracion de array linea {ctx.start.line}: la dimension debe ser mayor a 0")
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

    def enterMethodCall(self, ctx: decafParser.MethodCallContext):
        pass
        '''
        print(ctx.id_tok().getText())
        for i in ctx.arg():
            # arg es expression
            # puede ser location
            # puede ser methodCall
            # puede ser literal
            # puede ser expression op expression
            # etc
            print(i.getText())
            '''

    def enterStart(self, ctx: decafParser.StartContext):
        # Se crea el ambito global
        self.agregarAmbito()
        pilaFuncion.append({})

    def enterStructDeclaration(self, ctx: decafParser.StructDeclarationContext):
        self.agregarAmbito()

    def exitStructDeclaration(self, ctx: decafParser.StructDeclarationContext):
        self.quitarAmbito()

    def enterBlock(self, ctx: decafParser.BlockContext):
        self.agregarAmbito()
        if (len(ambitoVariableTemp) > 0):
            self.agregarAmbitoTempATabla()

    def exitBlock(self, ctx: decafParser.BlockContext):
        self.quitarAmbito()

    def exitStart(self, ctx: decafParser.StartContext):
        # este metodo se ejecuta al salir del ultimo nodo del arbol
        reglaMain = self.validarReglaMain()
        if (reglaMain):
            print(
                f"Error en linea {ctx.start.line}: {reglaMain}")


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
