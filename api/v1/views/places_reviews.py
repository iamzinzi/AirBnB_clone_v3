#!/usr/bin/python3
"""Create a new view for Review objects that handles all
default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def list_all_reviews(place_id):
    """Retrieves a list of all reviews of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    all_reviews = storage.all("Review").values()
    reviews = [r.to_dict() for r in all_reviews if r.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_a_review(review_id):
    """Retrieves a specific instance of Review, otherwise 404 error"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """Deletes a specific instance of Review, otherwise 404 error"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_reviews(place_id):
    """Adds another object to the storage"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    new_review_dict = request.get_json(silent=True)
    if new_review_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    elif 'text' not in request.json:
        return jsonify({'error': "Missing text"}), 400
    user = storage.get("User", request.json["user_id"])
    if user is None:
        abort(404)
    new_review_dict['place_id'] = place_id
    new_review = Review(**new_review_dict)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates an instance of review"""
    update_review_json = request.get_json(silent=True)
    if update_review_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for k, v in update_review_json.items():
        if k not in ignore:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
