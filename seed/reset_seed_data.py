import sys
import os
from app import create_app, db
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission
from sqlalchemy import text

# Tambahkan path ke folder app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Inisialisasi aplikasi Flask
app = create_app()

def reset_seed_data():
    """
    Reset data dan AUTO_INCREMENT untuk tabel role, permission, dan role_permission.
    Fungsi ini akan menghapus semua data di tabel tersebut dan mereset AUTO_INCREMENT ke 1.
    """
    with app.app_context():
        print("⚠️ Proses Reset Data Dimulai...")
        
        # Hapus data dari tabel role_permission, permission, dan role
        RolePermission.query.delete()
        Permission.query.delete()
        Role.query.delete()
        db.session.commit()

        # Reset AUTO_INCREMENT untuk setiap tabel
        db.session.execute(text("ALTER TABLE roles_permissions AUTO_INCREMENT = 1"))
        db.session.execute(text("ALTER TABLE permissions AUTO_INCREMENT = 1"))
        db.session.execute(text("ALTER TABLE roles AUTO_INCREMENT = 1"))
        db.session.commit()

        print("✅ Data di-reset dan AUTO_INCREMENT berhasil di-set ke 1.")

def prompt_for_confirmation():
    """
    Menanyakan kata kunci konfirmasi dari user sebelum melanjutkan reset data.
    """
    print("⚠️ Perhatian: Ini akan menghapus semua data pada tabel role, permission, dan role_permission!")
    user_input = input("Masukkan kata kunci untuk konfirmasi reset data (kata kunci: resetyuk2025): ")

    # Kata kunci konfirmasi yang diharapkan
    confirmation_keyword = "resetyuk2025"
    
    if user_input == confirmation_keyword:
        print("✅ Konfirmasi diterima, melanjutkan reset data...")
        reset_seed_data()
    else:
        print("❌ Konfirmasi salah. Proses dibatalkan.")

if __name__ == "__main__":
    prompt_for_confirmation()
