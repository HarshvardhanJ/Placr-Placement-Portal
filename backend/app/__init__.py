from flask import Flask
from .api import api_bp
from app.extensions import db, bcrypt, CORS, jwt
from app.config import Config
from app.utils.cli import register_commands
from app.models.user import User
from app.models.company import Company
from app.models.student import Student
from app.models.drive import Drive
from app.models.application import Application
from app.models.placement import Placement
from app.api.auth.routes import auth_bp
from app.api.admin.routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    register_commands(app)
    CORS(app)
    jwt.init_app(app)
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    return app
