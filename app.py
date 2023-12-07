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
colony = {} # Dictionary of cell colony grids, one for each user's session

# Define variables
# isRunning = False
# generation = 0
user_id = '298c5cba8e95ff110b1afcc307b712f83e8d245a46decc8c9a560bab8ef5c7fb' # Unique user session ID
tab_id = '0' # Unique browser tab ID

@app.route('/', methods=['GET', 'POST'])
def home():
    global colony, user_id, tab_id
    if request.method == 'POST':
        tab_id = request.form.get('tab_id')
        # If 'user_id' is not in the session or tab_id changed, generate a new user ID
        if 'user_id' not in session or tab_id != session.get('tab_id', '0'):
            # Remove the old user's session data from the colony dictionary
            # if 'user_id' in session and 'tab_id' in session and session['user_id']['tab_id'] in colony:
            #     del colony[session['user_id']][session['tab_id']]    
            if 'user_id' not in session: session['user_id'] = generate_user_id()
            # if 'tab_id' not in session: session['tab_id'] = tab_id
            colony[session['user_id']] = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS) # Create the cell colony grid and add it to the layout
        user_id = session['user_id']
        #check if the user id is in the colony dictionary
        if user_id not in colony or tab_id not in colony:
            colony[user_id] = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS)
        # return redirect(url_for('home'))
        return jsonify(user_id=user_id, tab_id=tab_id)  # Return JSON response
    else:
        return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS, user_id=user_id, tab_id=tab_id)

@app.route('/clear_session')
def clear_session():
    # Clear the user's session data
    if session['user_id'] in colony:
        del colony[session['user_id']]
    session.clear()
    return redirect(url_for('index'))

# Generate a unique user ID here
def generate_user_id():
    ip_address = request.remote_addr 
    current_time_ticks = int(time.time() * 1000) # Get current time in ticks (milliseconds)
    random_number = random.randint(1, 1000) # Generate a random number
    tab_id = session.get('tab_id', '0') # Use the tab_id from the session if it exists, otherwise use '0'
    unique_string = f"{ip_address}-{current_time_ticks}-{random_number}" # Combine IP address, time ticks and random number for uniqueness
    user_id = hashlib.sha256(unique_string.encode()).hexdigest() # Hash the unique string to create a consistent and secure user ID
    return user_id

# Start/Pause button clicked   
@app.route('/start', methods=['POST'])
def start_btn():
    # The "Start" button functionality here
    return jsonify({'result': 'Start button clicked!!!'})

# Generation increment timer event
@app.route('/increment', methods=['POST'])
def increment_generation():
    data = request.get_json()
    isRunning = data['isRunning']
    generation = data['generation']
    user_id = data['user_id']
    tab_id = data['tab_id']
    # if the game is running, increment the generation number and update the game state
    cell_ids = cell_states = []
    if isRunning:
        # cell_ids = ['cell-11-22', 'cell-0-0', 'cell-11-23']  # Example of an actual list of cell IDs
        # cell_states = [True, True, True]  # Example of an actual list of cell states
        cell_ids, cell_states = colony[user_id].go_through_one_generation()
    #return the list of cell IDs and states to update the game board
    return jsonify({'cell_ids': cell_ids, 'cell_states': cell_states, 'result': 'Generation incremented to ' + str(generation)})

# Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # "Clear" button functionality here
    data = request.get_json()
    user_id = data['user_id']
    tab_id = data['tab_id']    
    colony[user_id].clear_board()
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
    user_id = data['user_id']
    tab_id = data['tab_id']
    s_alive = 'alive' if alive else 'dead'
    colony[user_id].set_cell_state(col, row, alive)
    return jsonify({'result': f'Cell "{cell_id}" at row {row}, column {col} clicked {s_alive}'})

if __name__ == '__main__':
    app.run(debug=True)