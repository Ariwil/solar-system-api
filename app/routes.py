from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons

planets = [
    Planet(1, "Mars", "planet closest to the sun", ["Phobos", "Deimos"]), 
    Planet(2, "Venus", "hottest planet", "None"),
    Planet(3, "Earth", "planet with people", "moon")
]

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planet")

@planets_bp.route("", methods=["GET"])

def get_all_planets():
    response = []
    for planet in planets:
        this_one = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moons
        }
        response.append(this_one)
    return jsonify(response), 200