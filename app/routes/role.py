from config import Config
from extensions import db, jwt, create_access_token, jwt_required, get_jwt_identity, decode_token, get_jwt
from flask import Blueprint, jsonify, request
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission

role_bp = Blueprint('role', __name__)

@role_bp.route('/list', methods=['GET'])
# @jwt_required()
def list_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200
  
@role_bp.route('/create', methods=['POST'])
# @jwt_required()
def create_role():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
      
    if Role.query.filter_by(name=name).first():
        return jsonify({'error': 'Role already exists'}), 400
    
    new_role = Role(name=name)
    db.session.add(new_role)
    db.session.commit()
    
    return jsonify(new_role.to_dict()), 201

@role_bp.route('/delete/<int:role_id>', methods=['DELETE'])
# @jwt_required()
def delete_role(role_id):
    role = Role.query.get(role_id)
    
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    db.session.delete(role)
    db.session.commit()
    
    return jsonify({'message': 'Role deleted successfully'}), 200

@role_bp.route('/update/<int:role_id>', methods=['PUT'])
# @jwt_required()
def update_role(role_id):
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    role = Role.query.get(role_id)
    
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    
    role.name = name
    db.session.commit()
    
    return jsonify(role.to_dict()), 200
  
@role_bp.route('/assign-permission', methods=['POST'])
# @jwt_required()
def assign_permission():
    data = request.get_json()
    role_id = data.get('role_id')
    permission_ids = data.get('permission_id')

    if not role_id or not permission_ids:
        return jsonify({'error': 'Role ID and Permission IDs are required'}), 400

    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
      
    RolePermission.query.filter_by(role_id=role_id).delete()

    for pid in permission_ids:
        permission = Permission.query.get(pid)
        if not permission:
            return jsonify({'error': f'Permission with id {pid} not found'}), 404
        
        # Cek agar tidak double insert
        existing = RolePermission.query.filter_by(role_id=role.id, permission_id=permission.id).first()
        if not existing:
            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            db.session.add(role_permission)

    db.session.commit()

    return jsonify({'message': 'Permissions assigned successfully'}), 200

