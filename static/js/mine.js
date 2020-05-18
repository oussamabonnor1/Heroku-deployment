var request = require("request");

var options = {
  method: 'POST',
  url: 'https://sagemodeboy.eu.auth0.com/oauth/token',
  headers: {'content-type': 'application/x-www-form-urlencoded'},
  form: {
    grant_type: 'client_credentials',
    client_id: 'aotIkvWv0Kf7HikQEeW0EimtfA1RqPrN',
    client_secret: 'secret',
    audience: 'https://sagemodeboy.eu.auth0.com/api/v2/'
  }
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});