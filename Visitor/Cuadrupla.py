class Cuadrupla:

    def __init__(self, op=None, arg1=None, arg2=None, resultado=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.resultado = resultado

    def representacion(self):
        if(self.op == '='):
            return f"{self.resultado} = {self.arg1}"

        return f"{self.resultado} = {self.arg1} {self.op} {self.arg2}"

    def __repr__(self):
        return self.representacion()


if __name__ == '__main__':
    print(Cuadrupla(op='+', arg1='fp[0]', arg2='fp[4]', resultado='t0'))
    print(Cuadrupla(op='=', arg1='t1', resultado='G[0]'))
