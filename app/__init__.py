# Initializing things
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# init the app
app = Flask(__name__)

# link our config to our app
app.config.from_object(Config)

# init my Login Manager
login= LoginManager(app)
# send here when not logged in if trying to access login page
login.login_view='login'

# do inits for database stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import routes, models