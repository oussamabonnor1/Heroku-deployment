import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Agent
import sys

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
    def get_agents():
        agents = Agent.query.all()
        formatted_agents = [agent.format() for agent in agents]
        return jsonify({
            "agents":formatted_agents
        })

    @app.route('/get-agent/<id>')
    def get_agent(id):
        selected_agent = Agent.query.filter(Agent.id == id).one_or_none()
        if(selected_agent is None):
            return not_found(404)
        else: 
            return jsonify({
                "agents":selected_agent.format()
            })

    @app.route('/create-agent', methods=['POST'])
    def create_agent():
        body = request.get_json()
        try:
            person = Agent(name=body.get('name',''), age=body.get('age', ''), picture='')
            person.insert()
        except:
            print(sys.exc_info())
            db.session.rollback()
            return unprocessable(422)
        return get_agents()

    @app.route('/update-agent/<id>', methods=['PUT'])
    def update_agent(id):
        selected_agent = Agent.query.filter(Agent.id == id).one_or_none()
        if selected_agent is None:
            return not_found(404)
        else:
            body = request.get_json()
            name = body.get('name',selected_agent.name)
            age = body.get('age',selected_agent.age)
            picture = body.get('picture',selected_agent.picture)
            try:
                selected_agent.name = name 
                selected_agent.age = age
                selected_agent.picture = picture
                selected_agent.update()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_agents()

    @app.route('/delete-agent/<id>', methods=['DELETE'])
    def delete_agent(id):
        selected_agent = Agent.query.filter(Agent.id == id).one_or_none()
        if selected_agent is None:
            return not_found(404)
        else:
            try:
                selected_agent.delete()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_agents()

    #=================ERROR HANDLERS==================#
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
                        "success": False, 
                        "error": 403,
                        "message": "You don't have the permission to access the requested resource."
                        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "not found"
                        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
                        "success": False, 
                        "error": 500,
                        "message": "internal server error, check logs for more details"
                        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()