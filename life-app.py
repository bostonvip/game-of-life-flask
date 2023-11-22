# app.py
from flask import Flask, render_template, request, jsonify

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS)

#Start button clicked   
@app.route('/start', methods=['POST'])
def start_btn():
    # Your "Start" button functionality here
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
        # generation += 1
        # Your code to update the game state here
        pass

    return jsonify({'result': 'Generation incremented'})

#Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # Your "Clear" button functionality here
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