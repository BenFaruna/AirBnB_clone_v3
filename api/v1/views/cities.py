#!/usr/bin/python3
"""represensts the view for states"""
from flask import abort, jsonify, make_response, request

from api.v1.app import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """gets all the cities of a state present in the database"""
    data = storage.get(State, state_id)
    if not data:
        abort(404)

    cities = []
    for city in data.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """gets city in the database using its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a record from the database"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """post a new city to be added to storage"""
    data = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_city = City(**data)
    setattr(new_city, "state_id", state_id)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """updates the record  of an existing city"""
    data = request.get_json(silent=True)
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key != 'created_at' or key != 'updated_at':
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
