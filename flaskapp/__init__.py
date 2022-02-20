import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder="templates",static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'flaskapp/static/upload'
app.secret_key = os.urandom(42)

bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost/mapIT"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from flaskapp import views