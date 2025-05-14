import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import create_app, db
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission

# Buat instance aplikasi Flask
app = create_app()

with app.app_context():
    # Data seed
    roles = ["admin", "teacher", "student"]
    permissions = ["view_user", "edit_user", "delete_user", "manage_roles", "view_reports"]

    # Seed roles
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    # Seed permissions
    for perm_name in permissions:
        if not Permission.query.filter_by(name=perm_name).first():
            db.session.add(Permission(name=perm_name))

    db.session.commit()
    print("✅ Role dan permission berhasil di-seed.")
