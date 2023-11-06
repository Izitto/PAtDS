const { getCoords, getModels, populateCoords, populateModels, socketModels, socketCoords } = require('./vts_scripts.js');

getCoords();
getModels();
populateCoords();
populateModels();
socketCoords();
socketModels();

// ModelPositions should be fetched