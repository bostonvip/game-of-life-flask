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
    document.getElementById('start-button').addEventListener('click', () => {
        fetch('/start', {method: 'POST'})
            .then(response => response.json())
            // .then(data => console.log(data.result))
            .then(data => {
                console.log('New generation:', data.generation);
                document.getElementById('generation-label').textContent = 'Generation: ' + data.generation;
            });
    });

    document.getElementById('clear-button').addEventListener('click', () => {
        fetch('/clear', {method: 'POST'})
            .then(response => response.json())
            .then(data => console.log(data.result));
    });
});

