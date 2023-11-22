# app.py
from flask import Flask, render_template, request, jsonify

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS)

@app.route('/start', methods=['POST'])
def start_btn():
    # Your "Start" button functionality here
    # return jsonify({'result': 'Start button clicked!!!'})
    new_generation = 1  # Replace this with your actual new generation number
    return jsonify({'generation': new_generation})

@app.route('/clear', methods=['POST'])
def clear_btn():
    # Your "Clear" button functionality here
    return jsonify({'result': 'Clear button clicked!!!'})

@app.route('/cell_click', methods=['POST'])
def cell_click():
    data = request.get_json()
    cell_id = data['cell_id']
    row = data['row']
    col = data['col']
    # Your "cell_click" functionality here
    return jsonify({'result': f'Cell at row {row}, column {col} clicked'})

if __name__ == '__main__':
    app.run(debug=True)