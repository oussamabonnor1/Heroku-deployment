import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db,db, House, Agent, Job

class TestAppWrapper(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['HTTP_AUTHORIZATION'] = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56SkdOekF6UXpORFJqaENNekV6UlRCQlJVSTFSa1JEUkVKQ016VkZRek5DUWpCQk9FVXhOdyJ9.eyJpc3MiOiJodHRwczovL3NhZ2Vtb2RlYm95LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNzEzOTAzMTUzNjk3NzUxMTQxMiIsImF1ZCI6WyJDYXBzdG9uZUFQSSIsImh0dHBzOi8vc2FnZW1vZGVib3kuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4OTY3ODk0NCwiZXhwIjoxNTg5NzUwOTQ0LCJhenAiOiJhb3RJa3ZXdjBLZjdIaWtRRWVXMEVpbXRmQTFScVByTiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWdlbnRzIiwiZGVsZXRlOmhvdXNlcyIsImRlbGV0ZTpqb2JzIiwiZ2V0OmFnZW50cyIsImdldDpob3VzZXMiLCJnZXQ6am9icyIsInBvc3Q6YWdlbnRzIiwicG9zdDpob3VzZXMiLCJwb3N0OmpvYnMiLCJwdXQ6YWdlbnRzIiwicHV0OmhvdXNlcyIsInB1dDpqb2JzIl19.MX9WqKAVqZ2vlasS2-zbTM9ckuC1ARHqh5_DAhQpMovbAh_yl4PviFSgeInLtjPqtD_30b1B_3rJwKLjr66Cp2SA-Ftzx601SPYC5MTSbQBiHEbWDVzlG3ms4vtBF1-g4OdFoqDOab44RvtfNQkvotB4NSMF_4R8I8SCzllUvHv3LuKWtVcj5_URTK56wXp74Rz7fE299GDO7Ye1rK4SsLkSuSZK9gwzivDlwBCXmKxVEYstbljhQLpdREaooCQMuo8kzBKbjM1wu3b--iUQ5ONys53-BqbTQI0CNrwHxhwF4KF6zSKHQL3Uyb97OqGX1wMSKf-eeGqyvK-mfUN06g'
        return self.app(environ, start_response)

class CapstoneTest(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.wsgi_app = TestAppWrapper(self.app.wsgi_app)
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '','localhost:5432', self.database_name)
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    #=====================Success test area===============================
    #=====================Agents test area success========================
    def test_get_agents(self):
        res = self.client().get('/get-agents')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_agent(self):
        id = Agent.query.first().id
        res = self.client().get(f'/get-agent/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_agent(self):
        new_agent = {
            'name': 'some agent',
            'age': 27,
        }
        res = self.client().post('/create-agent', json = new_agent)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_agent(self):
        update_agent = {
            'name': 'some agent',
            'age': 27,
        }
        id = Agent.query.order_by(Agent.id.desc()).first().id
        res = self.client().put(f'/update-agent/{id}', json = update_agent)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        agent = Agent.query.filter(Agent.id == id).one_or_none()
        self.assertEqual(agent.age, update_agent["age"])

    def test_delete_agent(self):
        id = Agent.query.order_by(Agent.id.desc()).first().id
        res = self.client().delete(f'/delete-agent/{id}')
        data = json.loads(res.data)
        agent = Agent.query.filter(Agent.id == id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(agent, None)

    #=====================Houses test area success========================
    def test_get_houses(self):
        res = self.client().get('/get-houses')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_house(self):
        id = House.query.first().id
        res = self.client().get(f'/get-house/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_house(self):
        new_house = {
            'name': "some house",
            'rooms': 4,
            'price': 1525,
        }
        res = self.client().post('/create-house', json = new_house)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_house(self):
        update_house = {
            'name': "some house",
            'rooms': 5,
            'price': 1525,
        }
        id = House.query.order_by(House.id.desc()).first().id
        res = self.client().put(f'/update-house/{id}', json = update_house)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        house = House.query.filter(House.id == id).one_or_none()
        self.assertEqual(house.rooms, update_house["rooms"])

    def test_delete_house(self):
        id = House.query.order_by(House.id.desc()).first().id
        res = self.client().delete(f'/delete-house/{id}')
        data = json.loads(res.data)
        house = House.query.filter(House.id == id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(house, None)

    #=====================Jobs test area success========================
    def test_get_jobs(self):
        res = self.client().get('/get-jobs')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_create_job(self):
        self.test_create_agent()
        self.test_create_house()
        agent_id = Agent.query.order_by(Agent.id.desc()).first().id
        house_id = House.query.order_by(House.id.desc()).first().id

        new_job = {
            'agent_id': agent_id,
            'house_id': house_id
        }
        print(f"create job {new_job}")
        res = self.client().post('/create-job', json = new_job)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_csget_job(self):
        job = Job.query.order_by(Job.agent_id.desc()).first()
        print(f"get {job.agent_id}/{job.house_id}")
        res = self.client().get(f'/get-job?agent_id={job.agent_id}&house_id={job.house_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_cupdate_job(self):
        job = Job.query.order_by(Job.agent_id.desc()).first()
        print(f"update  {job.agent_id}/{job.house_id}")
        update_job = {
            'agent_id': job.agent_id,
            'house_id': job.house_id
        }
        res = self.client().put(f'/update-job?agent_id={job.agent_id}&house_id={job.house_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_job(self):
        self.test_create_job()
        job = Job.query.order_by(Job.agent_id.desc()).first()
        print(f"delete {job.agent_id}/{job.house_id}")
        res = self.client().delete(f'/delete-job?agent_id={job.agent_id}&house_id={job.house_id}')
        data = json.loads(res.data)
        job = Job.query.filter(Job.agent_id == job.agent_id and Job.house_id == job.house_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(job, None)

    #====================Test fail area=========================  
    #====================Test Agent area========================
    def test_get_agent_not_found(self):
        
        res = self.client().get('/get-agent/350')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_create_agent_not_allowed(self):
        new_agent = {
            'name': 'some agent',
            'age': 27,
        }
        res = self.client().post('/get-agents', json = new_agent)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method not allowed')

    def test_update_agent_not_found(self):
        update_agent = {
            'name': 'some agent',
            'age': 27,
        }
        id = 350
        res = self.client().put(f'/update-agent/{id}', json = update_agent)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_agent_not_found(self):
        id = 350
        res = self.client().delete(f'/delete-agent/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")

    #====================Test House area========================
    def test_get_house_not_found(self):
        
        res = self.client().get('/get-house/350')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_create_house_not_allowed(self):
        new_house = {
            'name': 'some house',
            'age': 27,
        }
        res = self.client().post('/get-houses', json = new_house)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method not allowed')

    def test_update_house_not_found(self):
        update_house = {
            'name': 'some house',
            'age': 27,
        }
        id = 350
        res = self.client().put(f'/update-house/{id}', json = update_house)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_house_not_found(self):
        id = 350
        res = self.client().delete(f'/delete-house/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")

    #====================Test Job area========================
    def test_get_job_not_found(self):
        
        res = self.client().get('/get-job?agent_id=350&house_id=350')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_create_job_not_allowed(self):
        new_job = {
             'agent_id': 1,
             'house_id': 1
        }
        res = self.client().post('/get-jobs', json = new_job)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method not allowed')

    def test_update_job_not_found(self):
        update_job = {
             'agent_id': 1,
             'house_id': 1
        }
        res = self.client().put(f'/update-job?agent_id=350&house_id=350', json = update_job)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_job_not_found(self):
        res = self.client().delete(f'/delete-job?agent_id=350&house_id=350')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()