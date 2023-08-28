// Call the keepAlive function when the page loads
$(document).ready(function() {
    keepAlive();
});

var neko_timer = getCookie('neko_timer') || 0;
var derp_timer = getCookie('derp_timer') || 0;
var derpSound = new Audio('/api/audio/derp.mp3');
var nekoSound = new Audio('/api/audio/nya.mp3');
var poofSound = new Audio('/api/audio/poof.mp3');
derpSound.loop = true;
nekoSound.loop = false;
poofSound.loop = false;
derpSound.volume = 0.3;
var neko_up = false;
var derp_up = false;
console.log("neko_timer: " + neko_timer + ", derp_timer: " + derp_timer);
var socket = io();

// Helper function for async getJSON
function getJsonAsync(url) {
    return new Promise((resolve, reject) => {
        $.getJSON(url, function (data) {
            resolve(data);
        }).fail(function (jqxhr, textStatus, error) {
            reject(error);
        });
    });
}

// Retrieve friend data when WebSocket message is received
socket.on('neko_timer_updated', async function () {
    try {
        const data = await getJsonAsync('/api/get_neko_timer');
        neko_timer += parseInt(data.timer);
    } catch (error) {
        console.error("Error retrieving neko_timer", error);
    }
});

// Retrieve viewer data when WebSocket message is received
socket.on('derp_timer_updated', async function () {
    try {
        const data = await getJsonAsync('/api/get_derp_timer');
        derp_timer += parseInt(data.timer);
    } catch (error) {
        console.error("Error retrieving derp_timer", error);
    }
});

function countdown() {
    // Update the neko timer
    if (neko_timer > 0) {
        neko_timer--;
        setCookie('neko_timer', neko_timer);
        if (neko_timer === 0) {
            document.getElementById("neko").classList.remove("up");
            if (neko_up) {
                neko_up = false;
                $.ajax({
                    type: "POST",
                    url: "/api/notify_neko",
                    data: {up: neko_up}
                });
                poofSound.play();
                nekoSound.pause();
            }
        }
        else if (neko_timer > 0) {
            document.getElementById("neko").classList.add("up");
            if (!neko_up) {
                neko_up = true;
                $.ajax({
                    type: "POST",
                    url: "/api/notify_neko",
                    data: {up: neko_up}
                });
                nekoSound.play();
            }
        }
        document.getElementById("neko").innerText = "Neko: " + neko_timer;
    }

    // Update the derp timer
    if (derp_timer > 0) {
        derp_timer--;
        setCookie('derp_timer', derp_timer);
        if (derp_timer === 0) {
            document.getElementById("derp").classList.remove("up");
            if (derp_up) {
                derp_up = false;
                $.ajax({
                    type: "POST",
                    url: "/api/notify_derp",
                    data: {up: derp_up}
                });
                derpSound.pause();
            }
        }
        else if (derp_timer > 0) {
            document.getElementById("derp").classList.add("up");
            if (!derp_up) {
                derp_up = true;
                $.ajax({
                    type: "POST",
                    url: "/api/notify_derp",
                    data: {up: derp_up}
                });
                derpSound.play();
            }
        }
        document.getElementById("derp").innerText = "Derp: " + derp_timer;
    }
}

// Call the countdown function every second
setInterval(countdown, 1000);

// Function to set a cookie
function setCookie(name, value) {
    console.log("Setting cookie: " + name + " = " + value);
    document.cookie = name + "=" + parseInt(value) + "; path=/";
}

// Function to get the value of a cookie
function getCookie(name) {
    var cookieName = name + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return null;
}
// This function will send a GET request to "/api/keep_alive" every 5 minutes
function keepAlive() {
    setInterval(function() {
        $.ajax({
            url: '/api/keep_alive?page=timer_overlay',
            type: 'GET',
            success: function(data) {
                console.log('Connection kept alive');
            },
            error: function(err) {
                console.error('Error in keepAlive:', err);
            },
        });
    }, 20000); // 20000 ms = 20 seconds
}

