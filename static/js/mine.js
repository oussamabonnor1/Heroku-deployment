
window.onload = function () {
  var parsedHash = new URLSearchParams(
    window.location.hash.substr(1) // skip the first char (#)
  );
  if(parsedHash.get('access_token') != null)
  window.localStorage.setItem("access_token",parsedHash.get('access_token'));
  if(window.localStorage.getItem('access_token') !== null){
    console.log("access: "+window.localStorage.getItem('access_token'));
    document.getElementById('login-bar').innerHTML = 'Refresh Token';
    document.getElementById('action-buttons').innerHTML += '<li class="last" style="margin-top: 10px;"><span class="call-us-box"><a id="logout-button" onclick="logout();" style="color: white;">Logout</a></span></li>'
  }
};
$('#call-properties').on('click', function () {
  openUrl('properties.html');
})

$('#call-agents').on('click', function () {
  openUrl('agents.html');
})

$('#call-jobs').on('click', function () {
  openUrl('jobs.html');
})

function openUrl(url) {
  var req = new XMLHttpRequest();
  req.open('GET', 'http://localhost:5000/'+url, true); //true means request will be async
  req.onreadystatechange = function (aEvt) {
    if (req.readyState == 4) {
      if (req.status == 200)
      //update your page here
      document.body.innerHTML = req.responseText;
     else
        if (req.status == 401)
          req.open('GET', '401');
        else alert("error of type "+ req.status);
    }
  };
  console.log(window.localStorage.getItem('access_token'));
  req.setRequestHeader('Authorization', 'Bearer '+ window.localStorage.getItem('access_token'));
  req.setRequestHeader('Access-Control-Allow-Origin', '*');
  req.setRequestHeader('Content-Type', 'application/json');
  req.send();
}

function logout() {
  window.localStorage.setItem("access_token",null);
  console.log(window.localStorage.getItem('access_token'));
  openUrl("");
}