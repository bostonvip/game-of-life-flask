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
user_id = '298c5cba8e95ff110b1afcc307b712f83e8d245a46decc8c9a560bab8ef5c7fb' # Unique user session ID
tab_id = '0' # Unique browser tab ID

@app.route('/', methods=['GET', 'POST'])
def home():
    global colony, user_id, tab_id
    if request.method == 'POST':
        tab_id = request.form.get('tab_id') #retrieve the tab_id from the form

        # if user_id is not in the session, generate a new user ID
        if 'user_id' not in session: 
            session['user_id'] = generate_user_id()

        # if user_id is not in the colony dictionary for the session user_id, add new tab_id dictionary to it
        if session['user_id'] not in colony:
            colony[session['user_id']] = {}
        user_id = session['user_id']            

        # if tab_id is not in the tab_id dictionary for the session user_id, create a new colony grid and add to it
        if tab_id not in colony[session['user_id']]:
            colony[session['user_id']][tab_id] = Colony(COLONY_NUMBER_OF_COLS, COLONY_NUMBER_OF_ROWS) # Create the cell colony grid and add it to the layout

        # return redirect(url_for('home'))
        return jsonify(user_id=user_id, tab_id=tab_id)  # Return JSON response
    else:
        return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS, user_id=user_id, tab_id=tab_id)

@app.route('/tab_closed', methods=['POST'])
def clear_session():
    # Clear the user's session data and remove the tab_id from the colony dictionary when the tab is closed
    data = request.get_json()
    user_id = data['user_id']
    tab_id = data['tab_id']
    print('Tab closed: ' + tab_id + ' for user: ' + user_id)
    if user_id in colony:
        if tab_id in colony[user_id]:
            del colony[user_id][tab_id]
            if len(colony[user_id]) == 0:
                del colony[user_id]
                session.clear()
    print('Colony length after: ' + str(len(colony)))
    return redirect(url_for('index'))

# Generate a unique user ID here
def generate_user_id():
    ip_address = request.remote_addr 
    current_time_ticks = int(time.time() * 1000) # Get current time in ticks (milliseconds)
    random_number = random.randint(1, 1000) # Generate a random number
    # tab_id = session.get('tab_id', '0') # Use the tab_id from the session if it exists, otherwise use '0'
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
        if user_id in colony and tab_id in colony[user_id]:
            cell_ids, cell_states = colony[user_id][tab_id].go_through_one_generation()
    #return the list of cell IDs and states to update the game board
    return jsonify({'cell_ids': cell_ids, 'cell_states': cell_states, 'result': 'Generation incremented to ' + str(generation)})

# Clear button clicked
@app.route('/clear', methods=['POST'])
def clear_btn():
    # "Clear" button functionality here
    data = request.get_json()
    user_id = data['user_id']
    tab_id = data['tab_id']
    if user_id in colony and tab_id in colony[user_id]:    
        colony[user_id][tab_id].clear_board()
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
    # update the cell state in the colony
    if user_id in colony and tab_id in colony[user_id]:
        colony[user_id][tab_id].set_cell_state(col, row, alive)
    return jsonify({'result': f'Cell "{cell_id}" at row {row}, column {col} clicked {s_alive}'})

if __name__ == '__main__':
    app.run(debug=True)