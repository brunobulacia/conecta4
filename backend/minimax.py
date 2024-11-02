# minimax.py
import random

class TreeNode:
    '''Clase para el árbol de decisiones'''
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


class Conecta4:
    def __init__(self):
        self.dificultad = ''
        self.profundidad_maxima = 4
        self.raiz = TreeNode([[]], None, 1)

    def set_dificultad(self, dificultad):
        self.dificultad = dificultad
        self.profundidad_maxima = 3 if dificultad == 'facil' else 4 if dificultad == 'medio' else 8

    def set_raiz(self, tablero):
        self.raiz = TreeNode(tablero, None, 1)
    
    def make_move(self, tablero, columna, jugador):
        '''Realiza la jugada en la columna dada y retorna un nuevo tablero.'''
        nuevo_tablero = [fila[:] for fila in tablero]
        for fila in range(5, -1, -1):
            if nuevo_tablero[fila][columna] is None:
                nuevo_tablero[fila][columna] = jugador
                break
        return nuevo_tablero

    def is_terminal_node(self, tablero):
        '''Verifica si el juego ha terminado (victoria o empate).'''
        return self.check_win(tablero, 1) or self.check_win(tablero, -1) or all(tablero[0][c] is not None for c in range(7))

    def check_win(self, tablero, jugador):
        '''Revisa si el jugador dado ha ganado en el tablero actual.'''
        for row in range(6):
            for col in range(7):
                if tablero[row][col] == jugador:
                    if (self.check_direction(tablero, row, col, 1, 0, jugador) or  # Horizontal
                        self.check_direction(tablero, row, col, 0, 1, jugador) or  # Vertical
                        self.check_direction(tablero, row, col, 1, 1, jugador) or  # Diagonal /
                        self.check_direction(tablero, row, col, 1, -1, jugador)):  # Diagonal \
                        return True
        return False

    def check_direction(self, tablero, row, col, row_dir, col_dir, jugador):
        '''Chequea si hay cuatro en línea en una dirección específica.'''
        count = 0
        for i in range(4):
            r = row + i * row_dir
            c = col + i * col_dir
            if 0 <= r < 6 and 0 <= c < 7 and tablero[r][c] == jugador:
                count += 1
            else:
                break
        return count == 4

    def evaluate_board(self, tablero):
        '''Evalúa el tablero y devuelve una puntuación según la posición del jugador y oponente.'''
        score = 0

        # Puntos adicionales para fichas en la columna central
        center_column = [row[3] for row in tablero]
        center_count = center_column.count(1)
        score += center_count * 3

        for row in range(6):
            for col in range(7):
                if tablero[row][col] is not None:
                    player = tablero[row][col]
                    score += self.evaluate_position(tablero, row, col, player)

        return score

    def evaluate_position(self, tablero, row, col, player):
        score = 0
        sequence_values = {2: 10, 3: 50, 4: 1000}
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row_dir, col_dir in directions:
            count = self.count_sequence(tablero, row, col, row_dir, col_dir, player)
            if count in sequence_values:
                score += sequence_values[count] if player == 1 else -sequence_values[count]

        return score

    def count_sequence(self, tablero, row, col, row_dir, col_dir, player):
        count = 0
        for i in range(4):
            r = row + i * row_dir
            c = col + i * col_dir
            if 0 <= r < 6 and 0 <= c < 7 and tablero[r][c] == player:
                count += 1
            else:
                break
        return count

    def minimax(self, tablero, profundidad, alpha, beta, maximizando):
        if profundidad == 0 or self.is_terminal_node(tablero):
            return self.evaluate_board(tablero), None

        if maximizando:
            mejor_puntuacion = float('-inf')
            mejor_columna = random.choice([c for c in range(7) if tablero[0][c] is None])
            for columna in range(7):
                if tablero[0][columna] is None:
                    nuevo_tablero = self.make_move(tablero, columna, 1)
                    puntuacion, _ = self.minimax(nuevo_tablero, profundidad - 1, alpha, beta, False)
                    if puntuacion > mejor_puntuacion:
                        mejor_puntuacion = puntuacion
                        mejor_columna = columna
                    alpha = max(alpha, puntuacion)
                    if alpha >= beta:
                        break
            return mejor_puntuacion, mejor_columna

        else:
            mejor_puntuacion = float('inf')
            mejor_columna = random.choice([c for c in range(7) if tablero[0][c] is None])
            for columna in range(7):
                if tablero[0][columna] is None:
                    nuevo_tablero = self.make_move(tablero, columna, -1)
                    puntuacion, _ = self.minimax(nuevo_tablero, profundidad - 1, alpha, beta, True)
                    if puntuacion < mejor_puntuacion:
                        mejor_puntuacion = puntuacion
                        mejor_columna = columna
                    beta = min(beta, puntuacion)
                    if alpha >= beta:
                        break
            return mejor_puntuacion, mejor_columna

    def get_best_move(self, tablero):
        _, columna = self.minimax(tablero, self.profundidad_maxima, float('-inf'), float('inf'), True)
        return columna