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
    roll_no = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    department = db.Column(db.String, nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    resume_path = db.Column(db.String, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    applications = db.relationship("Application", backref="student", lazy=True)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "user_id": self.user_id,
            "name": self.name,
            "roll_no": self.roll_no,
            "phone_number": self.phone_number,
            "department": self.department,
            "cgpa": self.cgpa,
            "year": self.year,
            "skills": self.skills,
            "experience": self.experience,
            "created_at": str(self.created_at),
        }
