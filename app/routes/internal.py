from flask import Blueprint, jsonify
from app.models.role import Role
from app import db
from flask_jwt_extended import decode_token
from flask import request

internal_role_bp = Blueprint('internal_role', __name__)

# @internal_role_bp.route('/permissions-by-role/<int:role_id>', methods=['GET'])
# def get_permissions_by_role(role_id):
#     role = Role.query.get(role_id)
#     if not role:
#         return jsonify({"error": "Role not found"}), 404
    
#     permissions = [p.name for p in role.permissions]
#     return jsonify({"permissions": permissions}), 200

@internal_role_bp.route('/role-name-by-role-id', methods=['GET'])
def get_role_name_by_role_id():
    role_id = request.args.get('role_id')
    if not role_id:
        return jsonify({"error": "role_id is required"}), 400

    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    return jsonify({"role_name": role.name}), 200


@internal_role_bp.route('/decode-token', methods=['POST'])
def decode_jwt():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded = decode_token(token)
        return jsonify(decoded), 200
    except Exception as e:
        return jsonify({"error": "Token decoding failed", "details": str(e)}), 400
