from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    from app.models.planet import Planets

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    return app
