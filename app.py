import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Agent

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ.get('EXCITED',False)
        greeting = "Welcome to the houses platform" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/get-agents')
    def be_cool():
        agents = Agent.query.all()
        formatted_agents = [agent.format() for agent in agents]
        return jsonify({
            "agents":formatted_agents
        })

    @app.route('/create-agent', methods=['POST'])
    def create_agent():
        body = request.get_json()
        person = Agent(name=body.get('name',''), age=body.get('age', ''))
        person.insert()
        return be_cool()





    return app

app = create_app()

if __name__ == '__main__':
    app.run()