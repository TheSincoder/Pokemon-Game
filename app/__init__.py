# Initializing things
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# init the app

login= LoginManager()
# do inits for database stuff
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    # init my Login Manager
    app.config.from_object(config_class)
    # link our config to our app

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # register plugins
    
    # send here when not logged in if trying to access login page
    login.login_view='auth.login'
    login.login_message = "Please Login to enter the PokeDevil Colosseum"
    login.login_message_category='warning'



    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    
    return app