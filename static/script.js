// static/script.js

// window.onload = function() {
//     var startButton = document.getElementById('start-button');
//     var clearButton = document.getElementById('clear-button');

//     startButton.addEventListener('click', function() {
//         // Add your "Start" button functionality here
//         // alert('Start button clicked');
//     });

//     clearButton.addEventListener('click', function() {
//         // Add your "Clear" button functionality here
//         // console.log('Clear button clicked');
//         // alert('Clear Button clicked!');
//     });
// };

document.addEventListener('DOMContentLoaded', (event) => {
    // const COLONY_NUMBER_OF_COLS = {{ num_of_cols | tojson }};

    // Get all grid cells
    const cells = document.querySelectorAll('.grid-cell');

    // Add click event listener to each cell
    cells.forEach((cell, index) => {
        cell.addEventListener('click', () => {
            // Toggle cell color
            cell.classList.toggle('black');

            // Calculate row and column
            const row = Math.floor(index / COLONY_NUMBER_OF_COLS);
            const col = index % COLONY_NUMBER_OF_COLS;

            // Send POST request to '/cell_click' route
            fetch('/cell_click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'cell_id': cell.id,  // Assuming each cell has a unique id
                    'row': row,
                    'col': col,
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data.result));
        });
    });
    
    let isRunning = false;

    document.getElementById('start-button').addEventListener('click', () => {
        isRunning = !isRunning;
        document.getElementById('start-button').textContent = isRunning ? 'Pause' : 'Start';
    
        fetch('/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ isRunning: isRunning }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('generation-label').textContent = 'Generation: ' + data.generation;
            console.log(data.result);
        });
    });

    document.getElementById('clear-button').addEventListener('click', () => {
        fetch('/clear', {method: 'POST'})
            .then(response => response.json())
            .then(data => console.log(data.result));
    });
});

