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
    # Data mapping: Role → list of permission names
    role_permissions_map = {
    "admin": [
        "class_control",
        "manage_role",
        "manage_profile",
        "manage_user",
        "assessment_session",
        "assessment_detail_student",
        "assignment_detail_student",
        "class_student_tab",
        "modify_assessment",
        "modify_question",
        "assessment_detail_teacher",
        "create_assessment",
        "assignment_detail_teacher",
        "class_student_tab_teacher",
        "class_detail",
        "view_class",
        "view_assessment",
        "get_item_pembelajaran"
    ],
    "teacher": [
        "manage_profile",
        "modify_assessment",
        "modify_question",
        "assessment_detail_teacher",
        "create_assessment",
        "assignment_detail_teacher",
        "class_student_tab_teacher",
        "class_detail",
        "view_class",
        "view_assessment",
        "get_item_pembelajaran"
    ],
    "student": [
        "manage_profile",
        "assessment_session",
        "assessment_detail_student",
        "assignment_detail_student",
        "class_student_tab",
        "view_class",
        "view_assessment",
        "get_item_pembelajaran"
    ],
    "guest": ["manage_profile"]
}


    for role_name, perm_names in role_permissions_map.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"⚠️ Role '{role_name}' not found, skip.")
            continue

        for perm_name in perm_names:
            perm = Permission.query.filter_by(name=perm_name).first()
            if not perm:
                print(f"⚠️ Permission '{perm_name}' not found, skip.")
                continue

            # Cek apakah relasi sudah ada
            existing = RolePermission.query.filter_by(role_id=role.id, permission_id=perm.id).first()
            if not existing:
                rp = RolePermission(role_id=role.id, permission_id=perm.id)
                db.session.add(rp)

    db.session.commit()
    print("✅ Role-permission seeding selesai.")
