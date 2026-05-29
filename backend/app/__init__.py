from flask import Flask
from .api import api_bp
from app.extensions import db, bcrypt
from app.config import Config
from app.utils.cli import register_commands
from app.models.user import User
from app.models.company import Company
from app.models.student import Student
from app.models.drive import Drive
from app.models.application import Application
from app.models.placement import Placement


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    register_commands(app)
    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
