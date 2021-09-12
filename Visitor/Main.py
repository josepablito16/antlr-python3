from typing import List
from antlr4 import *
from decafLexer import decafLexer
from decafVisitor import decafVisitor
from decafParser import decafParser

from Estructura import *
from Variable import *
from Funcion import *
from Error import *

# pilas donde se manejan los ambitos
pilaVariable = []
pilaFuncion = []
pilaEstructura = []


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

    def agregarAmbito(self, variable=True, estructura=False, funcion=False):
        '''
        Funcion para agregar un ambito

        Parametros:
        - variable: bool para indicar si se desea agregar un ambito de variables.
        - estructura: bool para indicar si se desea agregar un ambito de estructuras.
        - funcion: bool para indicar si se desea agregar un ambito de funciones.
        '''
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
        if variable:
            pilaVariable.pop({})
        if estructura:
            pilaEstructura.pop({})
        if funcion:
            pilaFuncion.pop({})

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

        # se elimina ambito global
        self.quitarAmbito(variable=True, funcion=True, estructura=True)
        return self.visitar(ctx.declaration())

    def visitStructDec(self, ctx: decafParser.StructDecContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # se elimina ambito de variable
        self.quitarAmbito()
        return super().visitStructDec(ctx)

    def visitMethodDec(self, ctx: decafParser.MethodDecContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # TODO agregar parametros al ambito

        # se elimina ambito de variable
        self.quitarAmbito()
        return ctx.id_tok().getText()

    def visitIfStmt(self, ctx: decafParser.IfStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # se elimina ambito de variable
        self.quitarAmbito()
        return super().visitIfStmt(ctx)

    def visitWhileStmt(self, ctx: decafParser.WhileStmtContext):
        # se crea ambito de variable
        self.agregarAmbito()

        # se elimina ambito de variable
        self.quitarAmbito()
        return super().visitWhileStmt(ctx)

    '''
    Declaracion de variable y arreglo
    '''

    def visitVarDec(self, ctx: decafParser.VarDecContext):
        nombre = ctx.id_tok().getText()
        tipo = ctx.varType().getText()
        print(f'visitVarDec {tipo} - {nombre}')
        errTemp = self.agregarVariableATabla(nombre, Variable(tipo))
        if isinstance(errTemp, Error):
            print(
                f"Error en declaracion de variable linea {ctx.start.line}: {errTemp.mensaje}")
        return super().visitVarDec(ctx)


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
