from config import Config
from extensions import db, jwt, create_access_token, jwt_required, get_jwt_identity, decode_token, get_jwt
from flask import Blueprint, jsonify, request
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission

permission_bp = Blueprint('permission', __name__)

@permission_bp.route('/list', methods=['GET'])
def list_permissions():
    try:
        permissions = Permission.query.all()
        return jsonify({
            'status': 'success',
            'message': 'Permissions retrieved successfully',
            'data': [permission.to_dict() for permission in permissions]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'message': f'Error retrieving permissions: {str(e)}',
            'data': None
        }), 500


@permission_bp.route('/create', methods=['POST'])
def create_permission():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({
            'status': 'failed',
            'message': 'Name is required',
            'data': None
        }), 400

    if Permission.query.filter_by(name=name).first():
        return jsonify({
            'status': 'failed',
            'message': 'Permission already exists',
            'data': None
        }), 400

    try:
        new_permission = Permission(name=name)
        db.session.add(new_permission)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Permission created successfully',
            'data': new_permission.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': f'Error creating permission: {str(e)}',
            'data': None
        }), 500


@permission_bp.route('/delete/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    permission = Permission.query.get(permission_id)

    if not permission:
        return jsonify({
            'status': 'failed',
            'message': 'Permission not found',
            'data': None
        }), 404

    permission_name = permission.name
    try:
        db.session.delete(permission)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Permission "{permission_name}" deleted successfully',
            'data': None
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': f'Error deleting permission: {str(e)}',
            'data': None
        }), 500


@permission_bp.route('/update/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({
            'status': 'failed',
            'message': 'Name is required',
            'data': None
        }), 400
    
    permission = Permission.query.get(permission_id)
    
    if not permission:
        return jsonify({
            'status': 'failed',
            'message': 'Permission not found',
            'data': None
        }), 404

    try:
        permission.name = name
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Permission with id {permission_id} updated successfully',
            'data': permission.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': f'Error updating permission: {str(e)}',
            'data': None
        }), 500