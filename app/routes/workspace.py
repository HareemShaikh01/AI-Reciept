from flask import Blueprint, jsonify, request
from app.services.workspace import create_workspace

workspace_bp = Blueprint("workspace_bp",__name__)


@workspace_bp.route("/v1/instances",methods=['POST'])
def create_workspace_route():
    # get auth token dummy for now
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    # extract from bearer
    token = auth_header.split(" ")[1]

    # get json input
    request_data = request.get_json()
    if not request_data or 'name' not in request_data:
        return jsonify({"error": "Missing workspace name"}), 400
    
    # extract name
    name = request_data['name']
    
    # 3. Call service
    result = create_workspace(name=name, token=token)
    
    return jsonify(result), 201
    
