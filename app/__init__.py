from flask import Flask
from extensions import jwt, migrate, db
from config import Config
from app.models.role import Role
from app.models.permissions import Permission
from app.models.role_permission import RolePermission
from app.routes.role import role_bp
from app.routes.permission import permission_bp
from app.routes.internal import internal_role_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)   
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(role_bp, url_prefix='/role')
    app.register_blueprint(permission_bp, url_prefix='/permission')
    app.register_blueprint(internal_role_bp, url_prefix='/internal')

    @app.route('/')
    def index():
        return 'ROLE MANAGEMENT Running!'

    return app
