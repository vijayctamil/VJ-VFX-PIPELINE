# Install dependencies: Flask, pymongo, pytest, requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["pipeline_db"]
projects_collection = db["projects"]

# File storage path
file_storage_path = "C:\\Users\\ADMIN\\Desktop\\VJ VFX PIPELINE\\ARCHITECTURE SETUP TEST\\storage\\"
if not os.path.exists(file_storage_path):
    os.makedirs(file_storage_path)

# API Endpoints
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = list(projects_collection.find({}, {'_id': 0}))
    return jsonify(projects), 200

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    projects_collection.insert_one(data)
    return jsonify({"msg": "Project created"}), 201

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file.save(os.path.join(file_storage_path, file.filename))
    return jsonify({"msg": "File uploaded"}), 202

if __name__ == "__main__":
    app.run(debug=True)
