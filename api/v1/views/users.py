#!/usr/bin/python3
"""Create a new view for User objects that handles all
default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.user import User


@app_views.route('/users/',
                 methods=['GET'],
                 strict_slashes=False)
def list_all_users():
    """Retrieves a list of all Users"""
    all_users = storage.all("User")
    users = [u.to_dict() for u in all_users.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """Retrieves a specific instance of User, otherwise 404 error"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_a_user(user_id):
    """Deletes a specific instance of User, otherwise 404 error"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Adds another object to the storage"""
    new_user_dict = request.get_json(silent=True)
    if new_user_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in request.json:
        return jsonify({'error': "Missing password"}), 400
    new_user = User(**new_user_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates an instance of User"""
    update_user_json = request.get_json(silent=True)
    if update_user_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'email']
    for k, v in update_user_json.items():
        if k not in ignore:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
