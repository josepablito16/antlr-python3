from typing import List
from antlr4 import *
from decafLexer import decafLexer
from decafVisitor import decafVisitor
from decafParser import decafParser

from Estructura import *
from Variable import *
from Funcion import *
from Error import *


from Nodo import Nodo
import Tipos as tipos

import copy

# pilas donde se manejan los ambitos
pilaVariable = []
pilaFuncion = []
pilaEstructura = []

FAIL = '\033[91m'
ENDC = '\033[0m'


class EvalVisitor(decafVisitor):

    def agregarVariableATabla(self, nombre, variable):
        '''
        Funcion que valida si una variable ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Parametros
        - nombre: string con el nombre de la variable
        - variable: objeto Variable con la informacion de la variable a ingresar.
        '''

        if(nombre in pilaVariable[-1].keys()):
            return Error('Esta variable ya existe')
        else:
            pilaVariable[-1][nombre] = variable

        print(f'''
                # Pila Variables
                {pilaVariable}
                ''')

    def agregarStructATabla(self, nombre, estructura):
        '''
        Funcion que valida si una estructura ya existe en la tabla actual
        si ya existe retorna error, caso contrario agrega a tabla (no retorna nada).

        Parametros
        - nombre: string con el nombre de la estructura
        - estructura: objeto estructura con la informacion de la estructura a ingresar.
        '''
        """
        print(f'''
        agregarStructATabla
        nombre = {nombre}
        pila = {pilaEstructura}
        ''')
        """
        if(nombre in pilaEstructura[-1].keys()):
            return Error(f"La estructura '{nombre}' ya ha sido declarada antes.")
        else:
            pilaEstructura[-1][nombre] = estructura

        print(f'''
                # Pila Estructura
                {pilaEstructura}
                ''')

    def validarEstructura(self, nombreEstructura):
        '''
        Funcion que valida si una estructura ya existe en la tabla actual
        si no existe retorna error, caso contrario True.

        Parametros
        - nombreEstructura: string con el nombre de la estructura
        '''
        if(nombreEstructura in pilaEstructura[-1].keys()):
            return True
        else:
            return Error(f"La estructura '{nombreEstructura}' no ha sido definida.")

    def agregarAmbito(self, variable=True, estructura=False, funcion=False):
        '''
        Funcion para agregar un ambito

        Parametros:
        - variable: bool para indicar si se desea agregar un ambito de variables.
        - estructura: bool para indicar si se desea agregar un ambito de estructuras.
        - funcion: bool para indicar si se desea agregar un ambito de funciones.
        '''
        print('agregarAmbito')
        if variable:
            pilaVariable.append({})
        if estructura:
            pilaEstructura.append({})
        if funcion:
            pilaFuncion.append({})

    def quitarAmbito(self, variable=True, estructura=False, funcion=False):
        '''
        Funcion para quitar un ambito

        Parametros:
        - variable: bool para indicar si se desea quitar un ambito de variables.
        - estructura: bool para indicar si se desea quitar un ambito de estructuras.
        - funcion: bool para indicar si se desea quitar un ambito de funciones.
        '''
        print('quitarAmbito')
        if variable:
            pilaVariable.pop()
        if estructura:
            pilaEstructura.pop()
        if funcion:
            pilaFuncion.pop()

    def visitar(self, tree):
        '''
        Funcion para visitar un arbol de antlr.

        Parametros:
        * tree: nodo raiz de antlr.

        Retorno:
        * Si la raiz tiene mas de un hijo retorna una lista con los resultados,
        caso contrario solo un resultado.
        '''
        if(isinstance(tree, list)):
            resultados = []
            for i in tree:
                resultados.append(self.visit(i))
            return resultados
        else:
            return self.visit(tree)

    def visitProgramStart(self, ctx: decafParser.ProgramStartContext):
        # se crea el ambito global
        self.agregarAmbito(variable=True, funcion=True, estructura=True)

        # visitamos todas las declaraciones del programa
        declaraciones = self.visitar(ctx.declaration())

        # se elimina ambito global
        self.quitarAmbito(variable=True, funcion=True, estructura=True)
        return declaraciones

    '''
    Declaracion de estructuras
    '''

    def visitStructDec(self, ctx: decafParser.StructDecContext):
        # se crea ambito de variable
        self.agregarAmbito()

        print('visitStructDec')
        nombre = ctx.id_tok().getText()
        self.visitar(ctx.varDeclaration())

        errTemp = self.agregarStructATabla(
            nombre, Estructura(copy.deepcopy(pilaVariable[-1])))

        if (isinstance(errTemp, Error)):
            print(
                f"{FAIL}Error en declaracion de estructura linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")

        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    '''
    Manejo de metodos
    '''

    def visitMethodDec(self, ctx: decafParser.MethodDecContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # TODO agregar parametros al ambito

        resultados = self.visitar(ctx.block())
        print('resultados')
        print(resultados)

        # se elimina ambito de variable
        self.quitarAmbito()
        return ctx.id_tok().getText()
    # TODO implementar methodCall

    '''
    Declaracion de variable y arreglo
    '''

    def visitVarDec(self, ctx: decafParser.VarDecContext):
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        errTemp = None
        esEstructura = False
        print(f'visitVarDec {tipo} - {nombre}')

        # Validar si es de tipo estructura
        if (tipo.find('struct') != -1):
            # es de tipo estructura
            tipo = tipo.replace('struct', '')

            errTemp = self.validarEstructura(tipo)
            if (isinstance(errTemp, Error)):
                print(
                    f"{FAIL}Error en declaracion de variable linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
                return
            esEstructura = True

        errTemp = self.agregarVariableATabla(
            nombre, Variable(tipo, isEstructura=esEstructura))
        if isinstance(errTemp, Error):
            print(
                f"{FAIL}Error en declaracion de variable linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
        return None

    def visitArrayDec(self, ctx: decafParser.ArrayDecContext):
        print('visitArrayDec')
        num = int(ctx.num().getText())
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        esEstructura = False

        # validar que num sea mayor a 0
        if not(num > 0):
            print(
                f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: la dimension debe ser mayor a 0")
            return

        # Validar si es de tipo estructura
        if (tipo.find('struct') != -1):
            # es de tipo estructura
            tipo = tipo.replace('struct', '')

            errTemp = self.validarEstructura(tipo)
            if (isinstance(errTemp, Error)):
                print(
                    f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")
                return
            esEstructura = True

        errTemp = self.agregarVariableATabla(
            nombre, Variable(tipo, isEstructura=esEstructura, long=num))
        if isinstance(errTemp, Error):
            print(
                f"{FAIL}Error en declaracion de array linea {ctx.start.line}{ENDC}: {errTemp.mensaje}")

        return None

    '''
    Manejo de literales
    '''

    def visitIntLiteral(self, ctx: decafParser.IntLiteralContext):
        # print('visitIntLiteral')
        # print(ctx.getText())
        return Nodo(tipos.INT, tipos.LITERAL)

    def visitCharLiteral(self, ctx: decafParser.CharLiteralContext):
        # print('visitCharLiteral')
        # print(ctx.getText())
        return Nodo(tipos.CHAR, tipos.LITERAL)

    def visitBoolLiteral(self, ctx: decafParser.BoolLiteralContext):
        # print('visitBoolLiteral')
        # print(ctx.getText())
        return Nodo(tipos.BOOLEAN, tipos.LITERAL)

    '''
    Manejo de llamada de variables
    '''

    def visitIdLocation(self, ctx: decafParser.IdLocationContext):
        nombre = ctx.id_tok().getText()
        tipo = tipos.getidLocationType(nombre, pilaVariable)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de variable linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.IDLOCATION)
        return Nodo(tipo, tipos.IDLOCATION)

    def visitArrayLocation(self, ctx: decafParser.ArrayLocationContext):
        nombre = ctx.id_tok().getText()
        expression = self.visitar(ctx.expression())

        # se valida que la variable exista y sea array
        tipo = tipos.getArrayLocationType(nombre, pilaVariable)
        if(isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

        # Se valida que expression sea de tipo int
        if (expression.tipo == tipos.INT):
            return Nodo(tipo, tipos.ARRAYLOCATION)
        else:
            print(
                f"{FAIL}Error en llamada de array linea {ctx.start.line}{ENDC}: exp no es de tipo 'int'")
            return Nodo(tipos.ERROR, tipos.ARRAYLOCATION)

    # TODO manejar idLocationDot
    # TODO manejar arrayLocationDot

    '''
    Manejo de statement
    '''

    def visitAssignmentStmt(self, ctx: decafParser.AssignmentStmtContext):
        location = self.visitar(ctx.location())
        expression = self.visitar(ctx.expression())
        tipo = tipos.validarTiposAsignacion(expression, location)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en asignacion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.ASSIGNMENT)
        else:
            return Nodo(tipo, tipos.ASSIGNMENT)

    def visitIfStmt(self, ctx: decafParser.IfStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    def visitWhileStmt(self, ctx: decafParser.WhileStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # se elimina ambito de variable
        self.quitarAmbito()
        return None

    '''
    Manejo de expresiones
    '''

    def manejarOperaciones(self, expres, ctx, tipoResultado, tipoOperandos):
        '''
        Funcion para manejar operaciones de tipo Arith '*'|'/'|'%'|'+'|'-'
        y tambien de tipo Rel '<'|'>'|'<='|'>='

        Parametros:
        - expres: lista de <Nodos>
        - ctx: contexto de la funcion donde se llama el metodo
        - tipoResultado: si la operacion sale bien, que tipo es el resultado

        Return:
        - objeto tipo <Nodo> con el resultado
        '''
        tipo = tipos.validarTiposOperacion(expres)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.OPERACION)

        else:
            if(tipo != tipoOperandos):
                print(
                    f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: No se puede usar el operador '{ctx.op.text}' con tipos de dato '{tipo}'")
                return Nodo(tipos.ERROR, tipos.OPERACION)
        return Nodo(tipoResultado, tipos.OPERACION)

    def visitFirstArithExpr(self, ctx: decafParser.FirstArithExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitSecondArithExpr(self, ctx: decafParser.SecondArithExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitRelExpr(self, ctx: decafParser.RelExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.INT)

    def visitEqExpr(self, ctx: decafParser.EqExprContext):
        expres = self.visitar(ctx.expression())
        tipo = tipos.validarTiposOperacion(expres)

        if (isinstance(tipo, Error)):
            print(
                f"{FAIL}Error en expresion linea {ctx.start.line}{ENDC}: {tipo.mensaje}")
            return Nodo(tipos.ERROR, tipos.OPERACION)

        return Nodo(tipos.BOOLEAN, tipos.OPERACION)

    def visitCondExpr(self, ctx: decafParser.CondExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.BOOLEAN)

    def visitNegativeExpr(self, ctx: decafParser.NegativeExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.INT, tipoOperandos=tipos.INT)

    def visitNotExpr(self, ctx: decafParser.NotExprContext):
        expres = self.visitar(ctx.expression())
        return self.manejarOperaciones(expres, ctx, tipoResultado=tipos.BOOLEAN, tipoOperandos=tipos.BOOLEAN)

    def visitParExpr(self, ctx: decafParser.ParExprContext):
        return self.visitar(ctx.expression())


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
