from app.extensions import db
import uuid
import enum


class UserRoleEnum(enum.Enum):
    admin = "admin"
    student = "student"
    company = "company"


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(UserRoleEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

    company_profile = db.relationship("Company", backref="user", uselist=False)
    student_profile = db.relationship("Student", backref="user", uselist=False)
