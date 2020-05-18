var access_token = '';
window.onload = function () {
  // var url = window.location.hash;
  // var access_token = new URLSearchParams(url.search).get('access_token');
  // console.log(access_token);
  var parsedHash = new URLSearchParams(
    window.location.hash.substr(1) // skip the first char (#)
  );
  if(parsedHash.get('access_token') != null)
  window.localStorage.setItem("access_token",parsedHash.get('access_token'));
  console.log(window.localStorage.getItem('access_token'));
};
$('#call-properties').on('click', function () {
  openUrl('properties');
})

$('#call-agents').on('click', function () {
  openUrl('agents');
})

$('#call-jobs').on('click', function () {
  openUrl('jobs');
})

function openUrl(url) {
  var req = new XMLHttpRequest();
  req.open('GET', 'http://localhost:5000/'+url+'.html', true); //true means request will be async
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