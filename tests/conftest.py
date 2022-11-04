import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planets

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    
    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def add_two_planets(app):
    planet1 = Planets(name="Mars", description="Planet closest to the sun", moons="Phobos, Deibos")
    planet2 = Planets(name="Venus", description="Hottest Planet", moons="No moons")

    db.session.add(planet1)
    db.session.add(planet2)
    db.session.commit()