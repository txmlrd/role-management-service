from flask import Flask
from extensions import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    jwt.init_app(app)
    
    @app.route('/')
    def index():
        return 'User Service Running!'

    return app
