from flask import Flask
from app.extensions import db, bcrypt, CORS, jwt, cache, mail
from app.config import Config
from app.utils.cli import register_commands
from app.api.auth.routes import auth_bp
from app.api.admin.routes import admin_bp
from app.api.company.routes import company_api
from app.api.student.routes import student_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    register_commands(app)
    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True,
    )
    jwt.init_app(app)
    cache.init_app(app)
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(company_api, url_prefix="/api/company")
    app.register_blueprint(student_api, url_prefix="/api/student")
    return app
