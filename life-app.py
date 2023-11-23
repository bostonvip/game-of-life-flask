# app.py
from flask import Flask, render_template, request, jsonify

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)

# Create the cell colony grid and add it to the layout
colony = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS)

@app.route('/')
def home():
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS)

#Start button clicked   
@app.route('/start', methods=['POST'])
def start_btn():
    # The "Start" button functionality here
    isRunning = request.get_json()['isRunning']
    #print(isRunning)
    #new_generation = 1  # Replace this with your actual new generation number
    return jsonify({'result': 'Start button clicked!!!'})

#Generation increment timer event
@app.route('/increment', methods=['POST'])
def increment_generation():
    data = request.get_json()
    isRunning = data['isRunning']
    generation = data['generation']

    if isRunning:
        # Your code to update the game state here
        cell_ids = ['cell-11-22', 'cell-0-0', 'cell-11-23']  # Replace this with your actual list of cell IDs
        cell_states = [True, True, True]  # Replace this with your actual list of cell states

    return jsonify({'cell_ids': cell_ids, 'cell_states': cell_states, 'result': 'Generation incremented'})

#Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # Ther "Clear" button functionality here
    return jsonify({'result': 'Clear button clicked!!!'})

#Cell clicked
@app.route('/cell_click', methods=['POST'])
def cell_click():
    data = request.get_json()
    cell_id = data['cell_id']
    row = data['row']
    col = data['col']
    # Your "cell_click" functionality here
    return jsonify({'result': f'Cell "{cell_id}" at row {row}, column {col} clicked'})

if __name__ == '__main__':
    app.run(debug=True)