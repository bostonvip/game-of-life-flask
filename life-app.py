# app.py
from flask import Flask, render_template

COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', num_of_rows = COLONY_NUMBER_OF_ROWS, num_of_cols = COLONY_NUMBER_OF_COLS)

if __name__ == '__main__':
    app.run(debug=True)