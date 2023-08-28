var viewer, friend, oldfriend, oldviewer;
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
socket.on('friend_updated', function () {
  $.getJSON('/api/friend', function (data) {
    friend = data.friend;
    if (friend != oldfriend && friend != '' && friend != null && friend != undefined) {
      connectAPI(friend);
    }
  });
});

// Retrieve viewer data when WebSocket message is received
socket.on('viewer_updated', function () {
  $.getJSON('/api/viewer', function (data) {
    viewer = data.viewer;
    if (viewer != oldviewer && viewer != '' && viewer != null && viewer != undefined) {
      displayViewerName(viewer);
    }
  });
});

console.log("friend: " + friend + ", viewer: " + viewer);




//everything below this works 100%
function connectAPI(name) {
  if (name === '' || name === null || name === undefined) {
    $('#user-profile').hide();
  }
  else {

    const twitchUrl = new URL(window.location.href);
    const username = twitchUrl.pathname.split('/')[1];
    $(document).ready(function () {
      // Replace with your Twitch API client ID and secret
      var clientId = 'a5exq8tkar569qgvzhf0eph02nxofa';
      var clientSecret = 'cemi9l9r89dgaou8ufvzbwmr84k35c';
      // Replace with the Twitch username you want to fetch
      var twitchUsername = name;
      // Get an access token from the Twitch API
      $.ajax({
        url: 'https://id.twitch.tv/oauth2/token',
        type: 'POST',
        data: {
          grant_type: 'client_credentials',
          client_id: clientId,
          client_secret: clientSecret
        },
        success: function (data) {

          // Use the access token to fetch the user's information from the Twitch API
          var accessToken = data.access_token;
          $.ajax({
            url: 'https://api.twitch.tv/helix/users',
            type: 'GET',
            headers: {
              'Authorization': 'Bearer ' + accessToken,
              'Client-Id': clientId
            },
            data: {
              login: twitchUsername
            },
            success: function (data) {
              // Display the user's profile picture and username on the page
              var profilePictureUrl = data.data[0].profile_image_url;
              var displayName = data.data[0].display_name;
              $('#user-profile').html('<img id="img" src="' + profilePictureUrl + '"><span id="name">' + displayName + ' is here</span>');
              $('#user-profile').css("box-shadow: 0px 0px 10px 5px rgb(184, 0, 0);");
              $('#user-profile').fadeIn();
              // Hide #user-profile after 2 seconds
              setTimeout(function () {
                $('#user-profile').fadeOut();
              }, 3000); // hide after 2 seconds
            },
            error: function (error) {
              console.log('Error fetching Twitch user information:', error);
            }
          });
        },
        error: function (error) {
          console.log('Error getting Twitch API access token:', error);
        }
      });
    });

  }
  oldfriend = name;
}
console.log("oldfriend: " + oldfriend);
//}
//console.log("starting socket and API connections");
//makeSocket();
console.log("Socket Started");


var viewerCount = 1;

function displayViewerName(name) {
  var newViewerSpan = $("<span>").attr("id", "viewer" + viewerCount).text(name + " is here");
  $("#viewers").prepend(newViewerSpan);
  newViewerSpan.css("opacity", "1");
  newViewerSpan.fadeIn();
  var newLine = $("<br>");
  $("#viewers").prepend(newLine);
  setTimeout(function () {
    newViewerSpan.animate({ opacity: 0 }, 1000, function () {
      $(this).remove();
      newLine.remove();
    });
  }, 1500); // fade out after 1.5 seconds
  oldviewer = name;
  viewerCount++;
}

// This function will send a GET request to "/api/keep_alive" every 5 minutes
function keepAlive() {
  setInterval(function() {
      $.ajax({
          url: '/api/keep_alive?page=friend_overlay',
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

