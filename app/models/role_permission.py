from app import db
from datetime import datetime
import uuid

class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    
    def to_dict(self):
        return {
            'role_id': self.role_id,
            'permission_id': self.permission_id
        }