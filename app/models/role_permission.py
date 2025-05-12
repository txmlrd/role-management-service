from app import db
from datetime import datetime
import uuid

class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'
    
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permissions_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)