from sqlalchemy.orm import backref

from app.extensions import db
import uuid
import enum


class StatusEnum(enum.Enum):
    approved = "approved"
    not_approved = "not_approved"


class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.user_id"), nullable=False, unique=True
    )
    name = db.Column(db.String, nullable=False, unique=True)
    contact = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)
    approval_status = db.Column(
        db.Enum(StatusEnum), nullable=False, default=StatusEnum.not_approved
    )
    industry = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    drives = db.relationship("Drive", backref="company", lazy=True)
