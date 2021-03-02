import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

DB_HOST = os.getenv('DB_HOST')  
DB_USER = os.getenv('DB_USER')  
DB_PASSWORD = os.getenv('DB_PASSWORD')  
DB_NAME = os.getenv('DB_NAME') 
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    SECRET_KEY = os.urandom(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
'''
Product

'''

class Product(db.Model):  
  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  description = db.Column(db.String)
  price = db.Column(db.String)
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))



  def __init__(self, name, description, price, category_id):
    self.name = name
    self.description = description
    self.price = price
    self.category_id = category_id

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
      'description': self.description,
      'price': self.price,
      'category_id': self.category_id
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String)
  description = db.Column(db.String)
  products = db.relationship('Product', backref='category', cascade="all,delete")


  def __init__(self, type, description):
    self.type = type
    self.description = description
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
      'type': self.type,
      'description': self.description
    }
    
