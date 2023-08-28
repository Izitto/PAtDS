document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect('http://' + document.domain + ':80');
    // ...
});
