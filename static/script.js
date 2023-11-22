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
    
    document.getElementById('start-button').addEventListener('click', () => {
        fetch('/start', {method: 'POST'})
            .then(response => response.json())
            // .then(data => console.log(data.result))
            .then(data => {
                // console.log('New generation:', data.generation);
                document.getElementById('generation-label').textContent = 'Generation: ' + data.generation;
            });
    });

    document.getElementById('clear-button').addEventListener('click', () => {
        fetch('/clear', {method: 'POST'})
            .then(response => response.json())
            .then(data => console.log(data.result));
    });
});

// window.onload = function() {
//     var grid = document.getElementById('grid-border');
//     var bottomContainer = document.getElementById('bottom-container');
//     bottomContainer.style.width = getComputedStyle(grid).width;
// }