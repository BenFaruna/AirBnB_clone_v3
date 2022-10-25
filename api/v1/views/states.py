#!/usr/bin/python3
"""represensts the view for states"""
from flask import abort, jsonify, make_response, request

from api.v1.app import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """gets all the states present in the database"""
    data = storage.all(State).values()
    states = []
    for state in data:
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """gets state in the database using its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a record from the database"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post a new state to be added to storage"""
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """updates the record  of an existing state"""
    data = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key != 'created_at' or key != 'updated_at':
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
