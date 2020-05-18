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
// $('#call-properties').on('click', function (e) {
//   e.preventDefault();
//   console.log('called');
//   $.ajax({
//     url: 'http://localhost:5000/properties.html',
//     type: 'GET',
//     contentType: 'application/json',
//     headers: {
//       'Authorization': this.access_token
//     },
//     async: false,
//     success: function (result) {
//       $(body).html(result);
//     },
//     error: function (error) {
//       console.log('error' + error);
//     }
//   });
// });
$('#call-properties').on('click', function (e) {
  var req = new XMLHttpRequest();
  req.open('GET', 'http://localhost:5000/properties.html', true); //true means request will be async
  req.onreadystatechange = function (aEvt) {
    if (req.readyState == 4) {
      if (req.status == 200)
      //update your page here
      document.body.innerHTML = req.responseText;
     else
        if (req.status == 401)
        alert("Unauthorized, please login first");
        else alert("error of type "+ req.status);
    }
  };
  console.log(window.localStorage.getItem('access_token'));
  req.setRequestHeader('Authorization', 'Bearer '+ window.localStorage.getItem('access_token'));
  req.setRequestHeader('Access-Control-Allow-Origin', '*');
  req.setRequestHeader('Content-Type', 'application/json');
  req.send();
})