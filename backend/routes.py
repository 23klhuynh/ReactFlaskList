
from flask import Blueprint, request, jsonify
from model import Friend, db

bp = Blueprint("main", __name__)

@bp.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200
    