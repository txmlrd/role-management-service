from flask import Flask
from extensions import jwt, migrate, db
from config import Config
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)   
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    @app.route('/')
    def index():
        return 'ROLE MANAGEMENT Running!'

    return app
