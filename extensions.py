import redis
from config import Config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token, get_jwt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)
jwt = JWTManager()
create_access_token = create_access_token
jwt_required = jwt_required
get_jwt_identity = get_jwt_identity
decode_token = decode_token
get_jwt = get_jwt
migrate = Migrate()
db = SQLAlchemy()

