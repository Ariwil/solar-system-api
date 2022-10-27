from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_TRACK_MODIFCATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres@localhost:5432/solar_system_development"

    from app.models.planet import Planets

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    return app
