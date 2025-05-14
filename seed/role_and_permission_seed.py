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
    # Seed roles dengan ID tetap
    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "teacher"},
        {"id": 3, "name": "student"},
        {"id": 4, "name": "guest"}
    ]

    # Seed permissions
    permissions = ["view_user", "edit_user", "delete_user", "manage_roles", "view_reports"]

    # Tambah roles
    for role in roles:
        db.session.add(Role(id=role["id"], name=role["name"]))

    # Tambah permissions
    for perm in permissions:
        db.session.add(Permission(name=perm))

    db.session.commit()
    print("✅ Roles dan permissions berhasil di-seed dengan ID tetap.")
