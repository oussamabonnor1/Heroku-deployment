from sqlalchemy import Column, String, create_engine,Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_name = "capstone"
database_path = os.environ["DATABASE_URL"] if os.environ.get("DEBUG", True) == False else "postgres://{}:{}@{}/{}".format('postgres', '','localhost:5432', database_name)

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


'''
Person
Have title and release year
'''
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

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'picture': self.picture
      }