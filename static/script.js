// static/script.js

document.addEventListener('DOMContentLoaded', (event) => {
    // Definitions
    let isRunning = false;
    let isBoardCleared = false;
    let generation = 0;
    const generation_update_interval = 500;  
    let timer = null;
    let user_id;
    let tab_id;  

    // Set tab_id and send it to the server
    if (!sessionStorage.getItem('tab_id')) {
        sessionStorage.setItem('tab_id', Date.now().toString());
    }
    tab_id = sessionStorage.getItem('tab_id');
    console.log('tab_id: ', tab_id);

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `tab_id=${tab_id}`,
    }) 
    .then(response => response.json())
    .then(data => {
        // Refresh user_id and tab_id
        user_id = data.user_id;
        tab_id = data.tab_id;
        console.log('user_id: ', user_id);

        // Update 'session-id-label' element on the DOM
        let sessionIdLabel = document.getElementById('session-id-label');
        sessionIdLabel.textContent = 'id: ' + user_id;
        sessionIdLabel.style.visibility = 'visible';
    });

    // Add event listener when the user closes the tab or browser
    window.addEventListener('beforeunload', (event) => {
        fetch('/tab_closed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'user_id': user_id, 'tab_id': tab_id}),
        });
        // .then(response => response.json())
        // .then(data => console.log(data.result));
    });

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
                    'alive': cell.classList.contains('black') ? 1 : 0,
                    'user_id': user_id,
                    'tab_id': tab_id
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data.result));
        });
    });
    
    // Add Start/Pause button and Generation Timer event listeners
    document.getElementById('start-button').addEventListener('click', () => {
        isRunning = !isRunning;
        document.getElementById('start-button').textContent = isRunning ? 'Pause' : 'Start';
    
        if (isRunning) {
            // Start the timer
            timer = setInterval(() => {
                generation++;
                document.getElementById('generation-label').textContent = 'Generation: ' + generation;
    
                fetch('/increment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({'isRunning': isRunning, 'generation': generation, 'user_id': user_id, 'tab_id': tab_id}),
                })
                .then(response => response.json())
                .then(data => {
                    // Update the grid
                    data.cell_ids.forEach((id, index0) => {
                        let cell = document.getElementById(id);
                        if (data.cell_states[index0] && isBoardCleared == false) {
                            cell.classList.add('black');
                        } else {
                            cell.classList.remove('black');
                        }
                    });
                    console.log(data.result);
                });
            }, generation_update_interval);
        } else {
            // Stop the timer
            clearInterval(timer);
        }

        fetch('/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'isRunning': isRunning, 'generation': generation, 'user_id': user_id, 'tab_id': tab_id}),
        })
        .then(response => response.json())
        .then(data => {
            isBoardCleared = false;
            console.log('The board is updating now!!!');
            console.log(data.result);
        });
        
    });

    // Add Clear button event listener
    document.getElementById('clear-button').addEventListener('click', () => {
        // Stop the timer
        if (timer) { clearInterval(timer); }
        // Clear the running state
        isRunning = false;
        // Reset the Start/Pause button
        document.getElementById('start-button').textContent = 'Start';
        // Reset the generation counter
        generation = 0;
        document.getElementById('generation-label').textContent = 'Generation: ' + generation;
        // Clear the grid
        cells.forEach((cell, index) => {
            cell.classList.remove('black');
        });
        console.log("The grid has been cleared!!!");
        isBoardCleared = true;
        console.log('The board is cleared now!!!');
        // Send POST request to '/clear' route
        fetch('/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'isRunning': isRunning, 'generation': generation, 'user_id': user_id, 'tab_id': tab_id}),
        })
        .then(response => response.json())
        .then(data => console.log(data.result));
    });
});

