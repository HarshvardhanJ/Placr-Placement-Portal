from sqlalchemy.orm import backref

from app.extensions import db
import uuid


class Student(db.Model):
    __tablename__ = "students"
    __table_args__ = (db.CheckConstraint("cgpa >= 0 AND cgpa <= 10"),)

    student_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.user_id"), nullable=False, unique=True
    )
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    department = db.Column(db.String, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    resume_path = db.Column(db.String, nullable=False)

    applications = db.relationship("Application", backref="student", lazy=True)
