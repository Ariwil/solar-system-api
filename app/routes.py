from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.planet import Planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planet")

def get_one_planet_or_abort(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        response_message = f"Error. {planet_id} must be an integer."
        abort(make_response(jsonify({"Message": response_message}), 400))

    matching_planet = Planets.query.get(planet_id)

    if matching_planet is None:
        response_message = f"Planet with id {planet_id} was not found in the database"
        abort(make_response(jsonify({"Message": response_message}), 404))

    return matching_planet

@planets_bp.route("", methods=["POST"])

def add_planet():
    request_body = request.get_json()
    print(request_body)
    new_planet = Planets(
        name=request_body["name"],
        description=request_body["description"],
        moons=request_body["moons"]
    )

    db.session.add(new_planet)
    db.session.commit() 

    return {"id": new_planet.id}, 201

@planets_bp.route("", methods=["GET"])

def get_all_planets():
    name_param = request.args.get("name")

    if name_param is None:
        planets = Planets.query.all()
    else:
        planets = Planets.query.filter_by(name=name_param)
        

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

@planets_bp.route("/<planets_id>", methods=["GET"])
def get_one_planet(planets_id):
    chosen_planet = get_one_planet_or_abort(planets_id)
    this_one = {
            "id": chosen_planet.id,
            "name": chosen_planet.name,
            "description": chosen_planet.description,
            "moons": chosen_planet.moons
        }

    return jsonify(this_one), 200

@planets_bp.route("/<planets_id>", methods=["PUT"])

def update_planet_with_new_data(planets_id):
    chosen_planet = get_one_planet_or_abort(planets_id)
    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "moons" not in request_body:
            return jsonify({"message": "Request must include name, description, and moons"}), 400
    
    chosen_planet.name = request_body["name"]
    chosen_planet.description = request_body["description"]
    chosen_planet.moons = request_body["moons"]

    db.session.commit()
    
    return jsonify({"message": f"Succesfully replaced planet with id '{planets_id}'"}), 200

@planets_bp.route("/<planets_id>", methods=["DELETE"])
def delete_one_planet(planets_id):
    chosen_planet = get_one_planet_or_abort(planets_id)
    db.session.delete(chosen_planet)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted planet with id {planets_id}"}), 200



