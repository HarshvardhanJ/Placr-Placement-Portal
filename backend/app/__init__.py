from flask import Flask
from .api import api_bp
from extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    bcrypt.init_app(app)
    # Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

