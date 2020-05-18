import os
from flask import Flask, render_template, request, abort, jsonify, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
from database.models import setup_db,db,House,Agent, Job
from auth.auth import requires_auth, AuthError
import json
import http

def create_app(test_config=None):

    login_url = f"https://sagemodeboy.eu.auth0.com/authorize?audience=CapstoneAPI&response_type=token&client_id=aotIkvWv0Kf7HikQEeW0EimtfA1RqPrN&redirect_uri={os.environ.get('CALLBACK','https://127.0.0.1:5000')}"

    token = os.environ.get("TOKEN","no token")

    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    setup_db(app)
    CORS(app)

    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/index.html')
    def index():
        return render_template('index.html')
    
    @app.route('/agents.html')
    def agents():
        agents = get_agents()
        return render_template('agents.html', data=agents.json)
    
    @app.route('/properties.html')
    def properties():
        houses = get_houses()
        return render_template('properties.html', data=houses.json)
    
    @app.route('/contact.html')
    def contact():
        return render_template('contact.html')
    
    @app.route('/jobs.html')
    def jobs():
        return render_template('jobs.html')

    @app.route('/login')
    def login():
        return redirect(login_url)

    #================== Agents Endpoints =====================
    @app.route('/get-agents')
    def get_agents():
        agents = Agent.query.all()
        formatted_agents = [agent.format() for agent in agents]
        return jsonify({
            "success":True,
            "agents":formatted_agents
        })

    @app.route('/get-agent/<id>')
    @requires_auth('get:agents')
    def get_agent(permission,id):
        selected_agent = Agent.query.filter(Agent.id == id).one_or_none()
        if(selected_agent is None):
            return not_found(404)
        else: 
            return jsonify({
                "success":True,
                "agents":selected_agent.format()
            })

    @app.route('/create-agent', methods=['POST'])
    @requires_auth('post:agents')
    def create_agent(permission):
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
    @requires_auth('put:agents')
    def update_agent(permission,id):
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
    @requires_auth('delete:agents')
    def delete_agent(permission,id):
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
            "success":True,
            "houses":formatted_houses
        })

    @app.route('/get-house/<id>')
    @requires_auth('get:houses')
    def get_house(permission,id):
        selected_house = House.query.filter(House.id == id).one_or_none()
        if(selected_house is None):
            return not_found(404)
        else: 
            return jsonify({
                "success":True,
                "agent":selected_house.format()
            })

    @app.route('/create-house', methods=['POST'])
    @requires_auth('post:houses')
    def create_house(permission):
        body = request.get_json()
        try:
            house = House(
                name=body.get('name',''),
                rooms=body.get('rooms', ''),
                price=body.get('price', ''),
                picture=body.get('picture', ''))
            house.insert()
        except:
            print(sys.exc_info())
            db.session.rollback()
            return unprocessable(422)
        return get_houses()

    @app.route('/update-house/<id>', methods=['PUT'])
    @requires_auth('put:houses')
    def update_house(permission, id):
        selected_house = House.query.filter(House.id == id).one_or_none()
        if selected_house is None:
            return not_found(404)
        else:
            body = request.get_json()
            name = body.get('name',selected_house.name)
            rooms = body.get('rooms',selected_house.rooms)
            price = body.get('price',selected_house.price)
            picture = body.get('picture',selected_house.picture)
            try:
                selected_house.name = name 
                selected_house.rooms = rooms
                selected_house.price = price
                selected_house.picture = picture
                selected_house.update()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_houses()

    @app.route('/delete-house/<id>', methods=['DELETE'])
    @requires_auth('delete:houses')
    def delete_house(permission, id):
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

    #================== Jobs Endpoints =====================
    @app.route('/get-jobs')
    @requires_auth('get:jobs')
    def get_jobs(permission):
        jobs = Job.query.all()
        formatted_jobs = [job.format() for job in jobs]
        return jsonify({
            "success":True,
            "jobs":formatted_jobs
        })

    @app.route('/get-job')
    @requires_auth('get:jobs')
    def get_job(permission):
        agent_id = request.args.get('agent_id',-1)
        house_id = request.args.get('house_id',-1)
        selected_job = Job.query.filter(Job.agent_id == agent_id and Job.house_id == house_id).one_or_none()
        if(selected_job is None):
            return not_found(404)
        else: 
            return jsonify({
                "success":True,
                "job":selected_job.format()
            })

    @app.route('/create-job', methods=['POST'])
    @requires_auth('post:jobs')
    def create_job(permission):
        body = request.get_json()
        try:
            job = Job(
                agent_id=body.get('agent_id',''),
                house_id=body.get('house_id', ''),
            )
            job.insert()
        except:
            print(sys.exc_info())
            db.session.rollback()
            return unprocessable(422)
        return get_jobs()

    @app.route('/update-job', methods=['PUT'])
    @requires_auth('put:jobs')
    def update_job(permission):
        agent_id = request.args.get('agent_id',-1)
        house_id = request.args.get('house_id',-1)
        selected_job = Job.query.filter(Job.agent_id == agent_id and Job.house_id == house_id).one_or_none()
        if selected_job is None:
            return not_found(404)
        else:
            try:
                selected_job.agent_id = agent_id 
                selected_job.house_id = house_id
                selected_job.update()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_jobs()

    @app.route('/delete-job', methods=['DELETE'])
    @requires_auth('delete:jobs')
    def delete_job(permission):
        agent_id = request.args.get('agent_id',-1)
        house_id = request.args.get('house_id',-1)
        selected_job = Job.query.filter(Job.agent_id == agent_id and Job.house_id == house_id).one_or_none()
        
        if selected_job is None:
            return not_found(404)
        else:
            try:
                selected_job.delete()
            except:
                print(sys.exc_info())
                db.session.rollback()
                return unprocessable(422)
            return get_jobs()

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

    @app.errorhandler(405)
    def forbidden(error):
        return jsonify({
                        "success": False, 
                        "error": 405,
                        "message": "Method not allowed"
                        }), 405

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