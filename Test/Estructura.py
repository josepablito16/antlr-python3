class Estructura:

    def __init__(self):
        self.campos = []

    '''
    Campo de tipo <Variable>
    '''

    def agregar(self, campo):
        self.campos.append(campo)

    def __repr__(self):
        return f"<Estructura>{self.campos}"
