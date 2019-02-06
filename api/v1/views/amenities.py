#!/usr/bin/python3
"""Create a new view for Amenity objects that handles all
default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_all_amenities():
    """Retrieves a list of all Amenities"""
    data = storage.all('Amenity')
    amenities = [v.to_dict() for k, v in data.items()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_specific_amenity(amenity_id):
    """Retrieves a specific instance of Amenity, otherwise 404 error"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_amenity(amenity_id):
    """Delete a specific instance of Amenity, otherwise 404 error"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Adds another object to the storage"""
    new_amenity_dict = request.get_json(silent=True)
    if new_amenity_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**new_amenity_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an instance of Amenity"""
    update_amenity_dict = request.get_json(silent=True)
    if update_amenity_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in update_amenity_dict.items():
        if k not in ignore:
            setattr(amenity, k, v)
            storage.save()
    return jsonify(amenity.to_dict())
