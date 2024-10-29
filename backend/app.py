# app.py
import random
from flask import Flask, request, jsonify as res
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/computer-move')
def computer_move():
    move = random.randint(1, 7)
    print('Computer move:' + str(move))
    return res({'move': move})

@app.route('/discs', methods=['PUT'])
def get_discs():
    data = request.get_json()
    matriz = data.get('matrix')
    print(matriz)
    return res({'matrix': matriz}), 200

@app.route('/submitForm', methods=['POST'])
def submit_form():
    data = request.get_json()
    difficulty = data.get('difficulty')
    starter = data.get('starter')
    print(f'Difficulty: {difficulty}, Starter: {starter}')
    return res({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True)