from config import Config
from extensions import db, jwt, create_access_token, jwt_required, get_jwt_identity, decode_token, get_jwt
from flask import Blueprint, jsonify, request
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission

permission_bp = Blueprint('permission', __name__)

@permission_bp.route('/list', methods=['GET'])
# @jwt_required()
def list_permissions():
    permissions = Permission.query.all()
    return jsonify([permission.to_dict() for permission in permissions]), 200
  
@permission_bp.route('/create', methods=['POST'])
# @jwt_required()
def create_permission():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
      
    if Permission.query.filter_by(name=name).first():
        return jsonify({'error': 'Permission already exists'}), 400
    
    new_permission = Permission(name=name)
    db.session.add(new_permission)
    db.session.commit()
    
    return jsonify(new_permission.to_dict()), 201
  
@permission_bp.route('/delete/<int:permission_id>', methods=['DELETE'])
# @jwt_required()
def delete_permission(permission_id):
    permission = Permission.query.get(permission_id)
    
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    db.session.delete(permission)
    db.session.commit()
    
    return jsonify({'message': 'Permission deleted successfully'}), 200
  
@permission_bp.route('/update/<int:permission_id>', methods=['PUT'])
# @jwt_required()
def update_permission(permission_id):
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    permission = Permission.query.get(permission_id)
    
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    permission.name = name
    db.session.commit()
    
    return jsonify(permission.to_dict()), 200
  


