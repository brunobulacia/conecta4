class Conecta4:
    def __init__(self):
        self.tablero = [[None for _ in range(7)] for _ in range(6)]
        self.jugada = 0
        self.dificultad = ''

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