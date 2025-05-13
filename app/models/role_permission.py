from app import db
from datetime import datetime
import uuid

class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    
    def to_dict(self):
        return {
            'roles_id': self.roles_id,
            'permissions_id': self.permissions_id
        }