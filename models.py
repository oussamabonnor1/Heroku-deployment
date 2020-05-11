from sqlalchemy import Column, String, create_engine,Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_name = "capstone"
database_path = os.environ.get("DATABASE_URL", "postgres://{}:{}@{}/{}".format('postgres', '','localhost:5432', database_name))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Agent(db.Model):  
  __tablename__ = 'Agents'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  picture = Column(String)

  def __init__(self, name, age, picture):
    self.name = name
    self.age = age
    self.picture = picture

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'picture': self.picture
      }

class House(db.Model):  
  __tablename__ = 'Houses'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  rooms = Column(Integer)
  price = Column(Integer)
  picture = Column(String)
  agent_id = db.Column(db.Integer, db.ForeignKey('Agents.id'))

  def __init__(self, name, rooms, price, picture, agent_id):
    self.name = name
    self.rooms = rooms
    self.price = price
    self.picture = picture
    self.agent_id = agent_id

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'rooms': self.rooms,
      'price': self.price,
      'agent': self.agent_id,
      'picture': self.picture
    }