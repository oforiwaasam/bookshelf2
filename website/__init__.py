from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Define a new database below
db = SQLAlchemy()
DB_NAME = "site.db"
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akdhej klklejio jh' 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize plugins
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