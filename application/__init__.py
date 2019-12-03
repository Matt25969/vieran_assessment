from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

user = os.getenv("FLASK_USER")
password = os.getenv("FLASK_PASSWORD")
host = os.getenv("FLASK_HOST")
database = os.getenv("FLASK_DB")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY2")

app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://"+user+":"+password+"@"+host+"/"+database)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes

