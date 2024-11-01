
class Conecta4:
    def __init__(self):
        self.tablero = [[None for _ in range(7)] for _ in range(6)]
        self.jugada = 0
        self.dificultad = 'easy'

class TreeNode:
    '''Clase para el arbol de decisiones'''
    def __init__(self, tablero, jugada, jugador):
        self.tablero = tablero
        self.jugada = jugada
        self.jugador = jugador
        self.hijos = []

    def get_tablero(self):
        return self.tablero
    
    def set_tablero(self, tablero):
        self.tablero = tablero
    
    def get_jugada(self):
        return self.jugada
    
    def set_jugada(self, jugada):
        self.jugada = jugada

    def get_dificultad(self):
        return self.dificultad
    
    def set_dificultad(self, dificultad):
        self.dificultad = dificultad

class Conecta4:
    def __init__(self):
        self.raiz = TreeNode([[None for _ in range(7)] for _ in range(6)], None, 'azul')
        self.dificultad = 'easy'
        self.profundidad_maxima = (
            3 if self.dificultad == 'facil' else
            4 if self.dificultad == 'medio' else
            8 # dificil 
        )
        self.build_tree(self.raiz, 0)

    def build_tree(self, nodo, profundidad):
        pass