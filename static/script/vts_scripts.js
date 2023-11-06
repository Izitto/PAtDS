var models = [];
var expressions = [];
var modelPositions = [
    {
        name: 'model name',
        id: 'model id',
        positions:
        [
            {
                name: 'position name',
                timeInSeconds: 'time in seconds',
                valuesAreRelativeToModel: 'relative',
                positionX: 'x',
                positionY: 'y',
                rotation: 'rotation',
                size: 'size'
            }
        ]
    }
];

var coords = {positionX: 0, positionY: 0, rotation: 0, size: 0};
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
        modelButton.setAttribute('modelname', model.name);
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
function socketModels() {
    // Listen for updates via Socket.io
    socket.on('vts_data_expressions', function(data) {
        if (data && Array.isArray(data)) {
            expressions = data;
            populateExpressions();
        } else {
            console.log('Failed to get expressions');
        }
    });
}
function socketExpressions() {
    socket.on('vts_data_models', function(data) {
        if (data && Array.isArray(data)) {
            models = data;
            populateModels();
        } else {
            console.log('Failed to get models');
        }
    });
}
function socketCoords() {
    socket.on('vts_data_coords', function(data) {
        if (data && typeof data === 'object') {
            coords = data;
            populateCoords();
        } else {
            console.log('Failed to get coords');
        }
    });
}


function getPositions() {
    fetch('/vts/api/modelPositions', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            modelPositions = data.modelPositions;
            populatePositions();
        } else {
            console.log('Failed to get positions, error: ' + data.error);
        }
    })
    .catch(error => {
        // do something
    });
}
/*
ModelPositions structure:
{
    "Model_Positions": [
        {
            "name": "model name",
            "id": "model id",
            "positions": [
                {
                    "name": "position name",
                    "timeInSeconds": "time in seconds",
                    "valuesAreRelativeToModel": "relative",
                    "positionX": "x",
                    "positionY": "y",
                    "rotation": "rotation",
                    "size": "size"
                }
            ]
        }
    ]
}
*/
// populate .positions-container div with position buttons, but only for which model id is active
/*
each button should have the position name as the innerHTML
do nothing for now when button is clicked
*/
function populatePositions() {
    const positionsContainer = document.querySelector('.position-container');
    positionsContainer.innerHTML = '';
    // modelPositions has name, id, positions[]
    // I want to populate this div with buttons for each position with modelPositions.positions[].name as the innerHTML where modelPositions.id == model-button[state="true"].getAttribute('modelId')
    // here
    modelPositions.forEach(modelPosition => {
        if (modelPosition.id == document.querySelector('.model-button[state="true"]').getAttribute('modelId')){
            modelPosition.positions.forEach(position => {
                console.log(position.name);
                const positionButton = document.createElement('button');
                positionButton.classList.add('position-button');
                positionButton.innerHTML = position.name;
                positionsContainer.appendChild(positionButton);
            });
        }
    });
}
/* if position button is clicked, populate the .position-data-container div with the position data in input fields with their ids set to the keys of the position data with the prefix "position-"
 if .add-pos button is clicked, populate the .position-data-container div with empty input fields

after the input fields, add a button called "set position" that when clicked, will get data from the coords object coords.positionX, coords.positionY, coords.rotation, coords.size and set it to the position data in the input fields with the prefix "position-"
no get request is needed get the model ID from the .model-button[state="true"] button and the position data the positions array where the name is the innerHTML of the position button
saving the position data will be done later
*/
function populatePositionData(){
    const positionDataContainer = document.querySelector('.position-data-container');
    positionDataContainer.innerHTML = '';
    const positionButton = document.querySelector('.position-button');
    if (positionButton){
        const positionName = positionButton.innerHTML;
        modelPositions.forEach(model => {
            if (model.id == document.querySelector('.model-button[state="true"]').getAttribute('modelId')) {
                // if one position button is pressed, populate the position data container with the position data for that position name
                // include position name, time in seconds, relative (checkbox), position x, position y, rotation, size
                // where modelPositions.id == model-button[state="true"].getAttribute('modelId') populate the position data container with the position data for that position name
                // model has no positions
                
            }
        });
    }
    const addPosButton = document.querySelector('.add-pos');
    positionDataContainer.innerHTML = '';
    if (addPosButton){
        addPosButton.addEventListener('click', () => {
            // add empty input fields for Name, Time in Seconds, Relative (checkbox), Position X, Position Y, Rotation (goes back to zero if bigger than 360 and back to 360 if smaller than zero), Size (limit to 100, -100)
            const positionNameInput = document.createElement('input');
            positionNameInput.classList.add('position-input');
            positionNameInput.setAttribute('type', 'text');
            positionNameInput.setAttribute('id', 'position-name');
            positionNameInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionNameInput);
            const positionTimeInput = document.createElement('input');
            positionTimeInput.classList.add('position-input');
            positionTimeInput.setAttribute('type', 'text');
            positionTimeInput.setAttribute('id', 'position-time');
            positionTimeInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionTimeInput);
            const positionRelativeInput = document.createElement('input');
            positionRelativeInput.classList.add('position-input');
            positionRelativeInput.setAttribute('type', 'checkbox');
            positionRelativeInput.setAttribute('id', 'position-relative');
            positionRelativeInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionRelativeInput);
            const positionXInput = document.createElement('input');
            positionXInput.classList.add('position-input');
            positionXInput.setAttribute('type', 'number');
            positionXInput.setAttribute('step', '0.001');
            positionXInput.setAttribute('id', 'position-positionX');
            positionXInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionXInput);
            const positionYInput = document.createElement('input');
            positionYInput.classList.add('position-input');
            positionYInput.setAttribute('type', 'number');
            positionYInput.setAttribute('step', '0.001');
            positionYInput.setAttribute('id', 'position-positionY');
            positionYInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionYInput);
            const positionRotationInput = document.createElement('input');
            positionRotationInput.classList.add('position-input');
            positionRotationInput.setAttribute('type', 'number');
            positionRotationInput.setAttribute('step', '0.001');
            positionRotationInput.setAttribute('min', '0');
            positionRotationInput.setAttribute('max', '360');
            positionRotationInput.setAttribute('id', 'position-rotation');
            positionRotationInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionRotationInput);
            const positionSizeInput = document.createElement('input');
            positionSizeInput.classList.add('position-input');
            positionSizeInput.setAttribute('type', 'number');
            positionSizeInput.setAttribute('step', '0.001');
            positionSizeInput.setAttribute('min', '-100');
            positionSizeInput.setAttribute('max', '100');
            positionSizeInput.setAttribute('id', 'position-size');
            positionSizeInput.setAttribute('value', '');
            positionDataContainer.appendChild(positionSizeInput);
            
        });
    }

    // set position button
    const setPositionButton = document.createElement('button');
    setPositionButton.classList.add('set-position-button');
    setPositionButton.innerHTML = 'Set Position';
    positionDataContainer.appendChild(setPositionButton);
    // if set position is clicked get coords.positionX, coords.positionY, coords.rotation, coords.size from the coords object in this file and set it to the position data in the input fields with the prefix "position-"
    setPositionButton.addEventListener('click', () => {
        for (const [key, value] of Object.entries(coords)) {
            if (key == 'positionX'){
                document.querySelector('#position-' + key).value = value;
            }else if (key == 'positionY'){
                document.querySelector('#position-' + key).value = value;
            }else if (key == 'rotation'){
                document.querySelector('#position-' + key).value = value;
            }else if (key == 'size'){
                document.querySelector('#position-' + key).value = value;
            }
        }
    });
}
// save button is .save-pos
// if save button is clicked, get the position data from the input fields with the prefix "position-" and send it to the server on the route /vts/api/saveModelPositions as a modelPositions object
// modelPositions object structure:
/*
{
    "Model_Positions": [
        {
            "name": "model name",
            "id": "model id",
            "positions": [
                {
                    "name": "position name",
                    "timeInSeconds": "time in seconds",
                    "valuesAreRelativeToModel": "relative",
                    "positionX": "x",
                    "positionY": "y",
                    "rotation": "rotation",
                    "size": "size"
                }
            ]
        }
    ]
}
*/
function saveModelPositions() {
    console.log('saveModelPositions');
    const savePosButton = document.querySelector('.save-pos');
    
    savePosButton.addEventListener('click', () => {
        console.log('save button clicked');
        const positionName = document.querySelector('#position-name').value;
        const positionTime = document.querySelector('#position-time').value;
        const positionRelative = document.querySelector('#position-relative').value;
        const positionX = document.querySelector('#position-positionX').value;
        const positionY = document.querySelector('#position-positionY').value;
        const positionRotation = document.querySelector('#position-rotation').value;
        const positionSize = document.querySelector('#position-size').value;
        const positionData = {
            'Model_Positions': [
                {
                    'name': positionName,
                    'id': document.querySelector('.model-button[state="true"]').getAttribute('modelId'),
                    'positions': [
                        {
                            'name': positionName,
                            'timeInSeconds': positionTime,
                            'valuesAreRelativeToModel': positionRelative,
                            'positionX': positionX,
                            'positionY': positionY,
                            'rotation': positionRotation,
                            'size': positionSize
                        }
                    ]
                }
            ]
        };
        // Create form data
        const formData = new URLSearchParams();
        formData.append('modelPositions', JSON.stringify(positionData));

        fetch('/vts/api/saveModelPositions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Model positions saved successfully');
            } else {
                console.log('Model positions failed to save, error: ' + data.error);
            }
        })
        .catch(error => {
            // do something
        });
    });

}
