import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Person

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = "true"
        #os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        people = Person.query.all()
        formatted_people = [person.format() for person in people]
        return jsonify({
            "people":formatted_people
        })

    @app.route('/create-person', methods=['POST'])
    def create_person():
        body = request.get_json()
        person = Person(name=body.get('name',''), catchphrase=body.get('catchphrase', ''))
        person.insert()
        return be_cool()





    return app

app = create_app()

if __name__ == '__main__':
    app.run()