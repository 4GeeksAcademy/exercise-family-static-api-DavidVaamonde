"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Jackson members
members_family = [
    {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
    },
    {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
    },
    {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
    }
]

# Bucle for para añadir miembros de la familia Jackson
for member in members_family:
    jackson_family.add_member(member)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Endpoint para listar todos los miembros de la familia Jackson
@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    # return jsonify(response_body), 200 <-- Devolvería el objeto response_body

    # Devolvemos JSON de la familia Jackson
    return jsonify(members), 200

# Endpoint para listar un miembro específico de la familia Jackson
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member), 200

# Endpoint para agregar un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data.get("first_name") or not data.get("age"):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_member = {
        "first_name": data["first_name"],
        "age" : data["age"],
        "lucky_numbers": data.get("lucky_numbers", []),
        "id": data.get("id", jackson_family._generateId())
    }

    jackson_family.add_member(new_member)

    return jsonify(new_member), 200


# Endpoint para eliminar un miembro de la familia
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    delete = jackson_family.delete_member(id)
    if not delete:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
