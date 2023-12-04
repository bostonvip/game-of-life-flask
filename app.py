# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from game_of_life import Colony
import random
import time
import hashlib

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'My.Very@Secret.Key'

# Create the cell colony grid and add it to the layout
colony = None #Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS)

# Define variables
isRunning = False
generation = 0

@app.route('/')
def home():
    global colony
    if 'user_id' not in session:
        # If 'user_id' is not in the session, generate a new user ID
        session['user_id'] = generate_user_id()
        colony = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS) # Create the cell colony grid and add it to the layout
    user_id = session['user_id']
    # if colony == None:
    #     colony = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS) # Create the cell colony grid and add it to the layout
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS, user_id=user_id)

@app.route('/clear_session')
def clear_session():
    # Clear the user's session data
    session.clear()
    return redirect(url_for('index'))

# Generate a unique user ID here
def generate_user_id():
    # Get the client's IP address
    ip_address = request.remote_addr

    # Get current time in ticks (milliseconds)
    current_time_ticks = int(time.time() * 1000)

    # Generate a random number
    random_number = random.randint(1, 1000)

    # Combine IP address, time ticks, and random number for uniqueness
    unique_string = f"{ip_address}-{current_time_ticks}-{random_number}"

    # Hash the unique string to create a consistent and secure user ID
    user_id = hashlib.sha256(unique_string.encode()).hexdigest()
    return user_id

# Start/Pause button clicked   
@app.route('/start', methods=['POST'])
def start_btn():
    # The "Start" button functionality here
    isRunning = request.get_json()['isRunning']
    return jsonify({'result': 'Start button clicked!!!'})

# Generation increment timer event
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

# Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # "Clear" button functionality here
    colony.clear_board()
    return jsonify({'result': 'Clear button clicked!!!'})

# Cell clicked
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