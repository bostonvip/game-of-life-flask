# app.py
from flask import Flask, render_template, request, jsonify
from game_of_life import Colony

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)

# Create the cell colony grid and add it to the layout
colony = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS)

# Define variables
isRunning = False
generation = 0

@app.route('/')
def home():
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS)

#Start/Pause button clicked   
@app.route('/start', methods=['POST'])
def start_btn():
    # The "Start" button functionality here
    isRunning = request.get_json()['isRunning']
    return jsonify({'result': 'Start button clicked!!!'})

#Generation increment timer event
@app.route('/increment', methods=['POST'])
def increment_generation():
    data = request.get_json()
    isRunning = data['isRunning']
    generation = data['generation']
    # if the game is running, increment the generation number and update the game state
    cell_ids = cell_states = []
    if isRunning:
        # cell_ids = ['cell-11-22', 'cell-0-0', 'cell-11-23']  # Example of an actual list of cell IDs
        # cell_states = [True, True, True]  # Example of an actual list of cell states
        cell_ids, cell_states = colony.go_through_one_generation()
    #return the list of cell IDs and states to update the game board
    return jsonify({'cell_ids': cell_ids, 'cell_states': cell_states, 'result': 'Generation incremented to ' + str(generation)})

#Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # "Clear" button functionality here
    colony.clear_board()
    return jsonify({'result': 'Clear button clicked!!!'})

#Cell clicked
@app.route('/cell_click', methods=['POST'])
def cell_click():
    # "Cell" clicked functionality here
    data = request.get_json()
    cell_id = data['cell_id']
    row = data['row']
    col = data['col']
    alive = data['alive']
    s_alive = 'alive' if alive else 'dead'
    colony.set_cell_state(col, row, alive)
    return jsonify({'result': f'Cell "{cell_id}" at row {row}, column {col} clicked {s_alive}'})

if __name__ == '__main__':
    app.run(debug=True)