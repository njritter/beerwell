# App settings and initialization.

from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# Give Flask-Login name of login view for redirecting not logged in users
# to the login form on pages with @login_required
login.login_view = 'login'

from app import routes, models # routes needs to import 'app' variable
