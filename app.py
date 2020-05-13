import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
from database.models import setup_db,db,House,Agent
from auth.auth import requires_auth, AuthError

def create_app(test_config=None):

    login_url = f"https://sagemodeboy.eu.auth0.com/authorize?audience=CapstoneAPI&response_type=token&client_id=aotIkvWv0Kf7HikQEeW0EimtfA1RqPrN&redirect_uri={os.environ.get('CALLBACK','https://127.0.0.1:5000/login')}"

    token = os.environ.get("TOKEN","no token")

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ.get('EXCITED',False)
        greeting = "Welcome to the houses platform " 
        greeting += "Endpoints: get-agents, get-houses "
        greeting += token
        print(os.environ.get("TEST",'no'))
        return greeting

    @app.route('/login')
    def login():
        return redirect(login_url)


    #================== Agents Endpoints =====================
    @app.route('/get-agents')
    @requires_auth('get:agents')
    def get_agents(permission):
        print(permission)
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


    #================== Houses Endpoints =====================
    @app.route('/get-houses')
    def get_houses():
        houses = House.query.all()
        formatted_houses = [house.format() for house in houses]
        return jsonify({
            "houses":formatted_houses
        })

    @app.route('/get-house/<id>')
    def get_house(id):
        selected_house = House.query.filter(House.id == id).one_or_none()
        if(selected_house is None):
            return not_found(404)
        else: 
            return jsonify({
                "agents":selected_house.format()
            })

    @app.route('/create-house', methods=['POST'])
    def create_house():
        body = request.get_json()
        try:
            house = House(
                name=body.get('name',''),
                rooms=body.get('rooms', ''),
                price=body.get('price', ''),
                picture=body.get('picture', ''),
                agent_id = body.get('agent', -1))
            house.insert()
        except:
            print(sys.exc_info())
            db.session.rollback()
            return unprocessable(422)
        return get_houses()

    @app.route('/update-house/<id>', methods=['PUT'])
    def update_house(id):
        selected_house = House.query.filter(House.id == id).one_or_none()
        if selected_house is None:
            return not_found(404)
        else:
            body = request.get_json()
            name = body.get('name',selected_house.name)
            rooms = body.get('rooms',selected_house.rooms)
            price = body.get('price',selected_house.price)
            picture = body.get('picture',selected_house.picture)
            agent_id = body.get('agent',selected_house.agent_id)
            try:
                selected_house.name = name 
                selected_house.rooms = rooms
                selected_house.price = price
                selected_house.picture = picture
                selected_house.agent_id = agent_id
                selected_house.update()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_houses()

    @app.route('/delete-house/<id>', methods=['DELETE'])
    def delete_house(id):
        selected_house = House.query.filter(House.id == id).one_or_none()
        if selected_house is None:
            return not_found(404)
        else:
            try:
                selected_house.delete()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_houses()

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
    
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": "Authorization header is expected."
                        }), 401
    return app

app = create_app()

if __name__ == '__main__':
    app.run()