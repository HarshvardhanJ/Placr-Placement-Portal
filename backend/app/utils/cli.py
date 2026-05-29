import click
from app.extensions import db, bcrypt
from app.models.user import User, RoleEnum


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        db.create_all()

        admin_user = User.query.filter_by(role=RoleEnum.admin).first()

        if not admin_user:
            admin_hashed_password = bcrypt.generate_password_hash("admin").decode(
                "utf-8"
            )
            admin_user = User(
                email="admin@admin.com",
                password=admin_hashed_password,
                role=RoleEnum.admin,
            )
            db.session.add(admin_user)
            db.session.commit()
