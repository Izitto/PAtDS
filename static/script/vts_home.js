var models = [];
var expressions = [];
var coords = {x: 0, y: 0, z: 0, r: 0}; // x, y, size, rotation
var socket = io(); // Initialize Socket.io connection

function getModels() {
    fetch('/vts/api/models', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            models = data.models;
            populateModels();
        } else {
            console.log('Failed to get models, error: ' + data.error);
        }
    })
    .catch(error => {
        // do something
    });
}

function getExpressions() {
    fetch('/vts/api/expressions', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            expressions = data.expressions;
            populateExpressions();
        } else {
            console.log('Failed to get expressions, error: ' + data.error);
        }
    })
    .catch(error => {
        // do something
    });
}

function getCoords() {
    fetch('/vts/api/coords', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            coords = data.coords;
            populateCoords();
        } else {
            console.log('Failed to get coords, error: ' + data.error);
        }
    })
    .catch(error => {
        // do something
    });
}



function populateModels() {
    const modelsContainer = document.querySelector('.models-container');
    modelsContainer.innerHTML = '';
    models.forEach(model => {
        const modelButton = document.createElement('button');
        modelButton.classList.add('model-button');
        modelButton.setAttribute('modelId', model.id);
        modelButton.setAttribute('state', model.active);
        if (model.active) {
            modelButton.style.backgroundColor = 'green';
        }
        modelButton.innerHTML = model.name;
        modelsContainer.appendChild(modelButton);

        // Set up the event listener for this button
        modelButton.addEventListener('click', () => {
            const Model_ID = modelButton.getAttribute('modelId');

            // Create form data
            const formData = new URLSearchParams();
            formData.append('Model_ID', Model_ID);

            fetch('/vts/api/loadModel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Model loaded successfully');
                } else {
                    console.log('Model failed to load, error: ' + data.error);
                }
            })
            .catch(error => {
                // do something
            });
        });
    });
}

function populateExpressions() {
    const expressionsContainer = document.querySelector('.expressions-container');
    expressionsContainer.innerHTML = '';
    expressions.forEach(expression => {
        const expressionButton = document.createElement('button');
        expressionButton.classList.add('expression-button');
        expressionButton.setAttribute('expressionfile', expression.file);
        expressionButton.setAttribute('state', expression.active);
        if (expression.active) {
            expressionButton.style.backgroundColor = 'green';
        }
        expressionButton.innerHTML = expression.name;
        expressionsContainer.appendChild(expressionButton);

        // Set up the event listener for this button
        expressionButton.addEventListener('click', () => {
            var Expression_File = expressionButton.getAttribute('expressionfile');
            var Expression_Active = false;
            if (expressionButton.getAttribute('state') == 'false'){
                Expression_Active = true;
            }else{
                Expression_Active = false;
            }

            // Create form data
            const formData = new URLSearchParams();
            formData.append('file', Expression_File);
            formData.append('active', Expression_Active);

            fetch('/vts/api/setExpression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Expression loaded successfully');
                } else {
                    console.log('Expression failed to load, error: ' + data.error);
                }
            })
            .catch(error => {
                // do something
            });
        });
    });
}

function populateCoords() {
    // populate the coords container div with noneditable input fields with 3 decimal places
    const coordsContainer = document.querySelector('.coords-container');
    coordsContainer.innerHTML = '';
    for (const [key, value] of Object.entries(coords)) {
        const coordInput = document.createElement('input');
        coordInput.classList.add('coord-input');
        coordInput.setAttribute('type', 'text');
        coordInput.setAttribute('id', key);
        coordInput.setAttribute('value', value.toFixed(3));
        coordInput.setAttribute('readonly', 'readonly');
        coordsContainer.appendChild(coordInput);
    }
}


// Fetch models and expressions only once
getCoords();
getModels();
getExpressions();

// Listen for updates via Socket.io
socket.on('vts_data_expressions', function(data) {
    if (data && Array.isArray(data)) {
        expressions = data;
        populateExpressions();
    } else {
        console.log('Failed to get expressions');
    }
});

socket.on('vts_data_models', function(data) {
    if (data && Array.isArray(data)) {
        models = data;
        populateModels();
    } else {
        console.log('Failed to get models');
    }
});

socket.on('vts_data_coords', function(data) {
    if (data && typeof data === 'object') {
        coords = data;
        populateCoords();
    } else {
        console.log('Failed to get coords');
    }
});

