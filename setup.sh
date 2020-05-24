export DATABASE_URL=postgres://postgres:@localhost:5432/capstone
export LOGIN_URL="https://sagemodeboy.eu.auth0.com/authorize?audience=CapstoneAPI&response_type=token&client_id=aotIkvWv0Kf7HikQEeW0EimtfA1RqPrN&redirect_uri=http://127.0.0.1:5000/"
export FLASK_APP=app.py
flask run --reload
