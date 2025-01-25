
from flask import Blueprint, request, jsonify
from model import Friend, db

bp = Blueprint("api", __name__)

#get friends
@bp.route("/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200
    
#create friend
@bp.route("/friends", methods=["POST"])
def create_friend():
    try:
        data = request.json

        required_fields = ["name", "role", "description", "gender"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        #fetch avater image
        if gender == "male":
           img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
           img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
           img_url = None
        
        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_friend)

        db.session.commit()

        return jsonify({"message": "Friend create successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

#delete
@bp.route("/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)

        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message": "Friend delete successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update a friend profile
@bp.route("/friends/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)

        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        
        data = request.json

        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)

        db.session.commit()

        return jsonify({"message": "Update successfully"})


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
