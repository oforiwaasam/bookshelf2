from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Define a new database below
db = SQLAlchemy()
DB_NAME = "site.db"
login_manager = LoginManager()

def create_app():
    # database configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akdhej klklejio jh' 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # path to database and its name
    #to disable a feature that signals the application every time a 
    # change is about to be made in the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Initialize plugins with our application
    db.init_app(app)
    login_manager.init_app(app)

    from . import routes
    from . import auth

     # Register Blueprints
    app.register_blueprint(routes.main)
    app.register_blueprint(auth.auth)

    from .models import User, Note

    create_database(app)

    return app

# you can also create the database here
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')