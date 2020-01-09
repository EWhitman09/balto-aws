import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

#Grab postgres info from RDS env vars
HOSTNAME = os.environ.get('RDS_HOSTNAME')
PORT = os.environ.get('RDS_PORT')
DB_NAME = os.environ.get('RDS_DB_NAME')
USERNAME = os.environ.get('RDS_USERNAME')
PASSWORD = os.environ.get('RDS_PASSWORD')

application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DB_NAME)

db = SQLAlchemy(application)


class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))

  def __init__(self, name, email):
    self.name = name
    self.email = email
	
db.create_all()

@application.route('/', methods=['GET'])
def index():
  return render_template('index.html', users=User.query.all())


@application.route('/user', methods=['POST'])
def user():
  u = User(request.form['name'], request.form['email'])
  db.session.add(u)
  db.session.commit()
  return redirect(url_for('index'))