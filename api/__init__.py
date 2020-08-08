from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('api.config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rubik1000@localhost:5430/postgres'
db = SQLAlchemy(app)
app.secret_key = 'some_random_key'

import api.routes.views
import api.models.db_creation

db.create_all()
