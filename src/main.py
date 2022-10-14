"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites_people, Favorites_planet, Favorites_vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#****************USERS********************
#-----------------------------------------
@app.route('/user', methods=['GET'])
def get_users():
    user = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), user))
    response_body = {
        "usuarios": result,
        "msg": "Ususarios"
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200

#****************PEOPLE********************
#------------------------------------------

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.filter().all()
    result = list(map(lambda character: character.serialize(), people))
    return jsonify(result), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = People.query.get(people_id)
    return jsonify(character.serialize()), 200



#****************PLANETS********************
#-------------------------------------------

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.filter().all()
    result = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet.serialize()), 200

#****************VEHICLES********************
#--------------------------------------------

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.filter().all()
    result = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return jsonify(result), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    return jsonify(vehicle.serialize()), 200


#****************FAVORITES********************
#---------------------------------------------

@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    planets = Favorites_planet.query.filter().all()
    people = Favorites_people.query.filter().all()
    vehicles = Favorites_vehicles.query.filter().all()
    result = list(map(lambda planet: planet.serialize(), planets)),
    list(map(lambda character: character.serialize(), people)),
    list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return jsonify(result), 200

#****************FAV PEOPLE********************
#----------------------------------------------

@app.route('/user/favorites/people', methods=['GET'])
def get_fav_people():
     people = Favorites_people.query.filter().all()
     result = list(map(lambda character: character.serialize(), people))
     return jsonify(result), 200

@app.route('/user/favorites/people/<int:user_id>/<int:people_id>', methods=['POST'])
def add_fav_people(user_id, people_id):
    fav_people = Favorites_people(user_id=int(user_id), people_id=int(people_id))
    db.session.add(fav_people)
    db.session.commit()
    response_body = {
        "msg": "Favorito agregado"
    }
    return jsonify(response_body), 200


#****************FAV PLANETS********************
#-----------------------------------------------

@app.route('/user/favorites/planets', methods=['GET'])
def get_fav_planet():
    planets = Favorites_planet.query.filter().all()
    result = list(map(lambda planet: planet.serialize(), planets))
    return {"msj":"Planets response"} # jsonify(result), 200

@app.route('/user/favorites/planets/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_fav_planet(user_id, planet_id):
    fav_planet = Favorites_planet(user_id=int(user_id), planet_id=int(planet_id))
    db.session.add(fav_planet)
    db.session.commit()
    response_body = {
        "msg": "Favorito agregado"
    }
    return jsonify(response_body), 200

#****************FAV VEHICLES********************
#------------------------------------------------

@app.route('/user/favorites/vehicles', methods=['GET'])
def get_fav_vehicles():
    vehicles = Favorites_vehicles.query.filter().all()
    result = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return {"msj":"Vehicles response"} #jsonify(result), 200, 

@app.route('/user/favorites/vehicles/<int:user_id>/<int:vehicles_id>', methods=['POST'])
def add_fav_vehicle(user_id, vehicles_id):
    fav_vehicle = Favorites_vehicles(user_id=int(user_id), vehicles_id=int(vehicles_id))
    db.session.add(fav_vehicle)
    db.session.commit()
    response_body = {
        "msg": "Favorito agregado"
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
