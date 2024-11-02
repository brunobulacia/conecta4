# app.py
import random
from flask import Flask, request, jsonify as res
from flask_cors import CORS
from minimax import Conecta4



starter = None

game = Conecta4()

app = Flask(__name__)
CORS(app)

matriz = [[None for _ in range(7)] for _ in range(6)]

@app.route('/computer-move')
def computer_move():
    if matriz is not None:
        move = game.get_best_move(matriz)
    else: 
        move = game.get_best_move([[None for _ in range(7)] for _ in range(6)])
    return res({'move': move})

@app.route('/discs', methods=['PUT'])
def get_discs():
    data = request.get_json()
    global matriz
    matriz = data.get('matrix')
    game.set_raiz(matriz)
    print(game.dificultad)
    return res({'matrix': game.raiz.get_tablero()}), 200

@app.route('/submitForm', methods=['POST'])
def submit_form():
    data = request.get_json()
    difficulty = data.get('difficulty')
    global starter
    starter = data.get('starter')
    game.set_dificultad(difficulty)
    print(f'Difficulty: {game.dificultad}, Starter: {starter}')
    return res({'success': True}), 200


@app.route('/starter', methods=['GET'])
def whoStarts():
    return res({'starter': starter})


if __name__ == '__main__':
    app.run(debug=True)


