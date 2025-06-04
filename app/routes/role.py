from config import Config
from extensions import db, jwt, create_access_token, jwt_required, get_jwt_identity, decode_token, get_jwt
from flask import Blueprint, jsonify, request
from app.models.role import Role

role_bp = Blueprint('role', __name__)

@role_bp.route('/list', methods=['GET'])
def list_roles():
    try:
        roles = Role.query.all()
        role_data = [role.to_dict() for role in roles]
        return jsonify({
            "status": "success",
            "message": "Role list fetched successfully",
            "data": role_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": f"Failed to fetch role list: {str(e)}",
            "data": None
        }), 500

  
@role_bp.route('/create', methods=['POST'])
def create_role():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({
            'status': 'failed',
            'message': 'Name is required',
            'data': None
        }), 400

    if Role.query.filter_by(name=name).first():
        return jsonify({
            'status': 'failed',
            'message': 'Role already exists',
            'data': None
        }), 400

    try:
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Role created successfully',
            'data': new_role.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': f'Error creating role: {str(e)}',
            'data': None
        }), 500


@role_bp.route('/delete/<int:role_id>', methods=['DELETE'])
# @jwt_required()
def delete_role(role_id):
    role = Role.query.get(role_id)
    
    if not role:
        return jsonify({
            'status': 'failed',
            'message': 'Role not found',
            'data': None
        }), 404
    role_name = role.name
    db.session.delete(role)
    db.session.commit()
    
    return jsonify({
            'status': 'success',
            'message': f'Role {role_name} deleted successfully',
            'data': None
        }), 200

@role_bp.route('/update/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({
            'status': 'failed',
            'message': 'Name is required',
            'data': None
        }), 400
    
    role = Role.query.get(role_id)
    
    if not role:
        return jsonify({
            'status': 'failed',
            'message': 'Role not found',
            'data': None
        }), 404

    try:
        role.name = name
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Role with id {role_id} updated successfully',
            'data': role.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': f'Error updating role: {str(e)}',
            'data': None
        }), 500

  
# @role_bp.route('/assign-permission', methods=['POST'])
# def assign_permission():
#     data = request.get_json()
#     role_id = data.get('role_id')
#     permission_ids = data.get('permission_id')

#     if not role_id or not permission_ids:
#         return jsonify({
#             'status': 'failed',
#             'message': 'Role ID and Permission IDs are required',
#             'data': None
#         }), 400

#     role = Role.query.get(role_id)
#     if not role:
#         return jsonify({
#             'status': 'failed',
#             'message': 'Role not found',
#             'data': None
#         }), 404

#     try:
#         RolePermission.query.filter_by(role_id=role_id).delete()

#         for pid in permission_ids:
#             permission = Permission.query.get(pid)
#             if not permission:
#                 return jsonify({
#                     'status': 'failed',
#                     'message': f'Permission with id {pid} not found',
#                     'data': None
#                 }), 404

#             existing = RolePermission.query.filter_by(
#                 role_id=role.id, permission_id=permission.id
#             ).first()

#             if not existing:
#                 role_permission = RolePermission(
#                     role_id=role.id, permission_id=permission.id
#                 )
#                 db.session.add(role_permission)

#         db.session.commit()

#         return jsonify({
#             'status': 'success',
#             'message': 'Permissions assigned successfully',
#             'data': {
#                 'role_id': role.id,
#                 'assigned_permissions': permission_ids
#             }
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'status': 'failed',
#             'message': f'Error assigning permissions: {str(e)}',
#             'data': None
#         }), 500


