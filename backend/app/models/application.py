from app.extensions import db
import uuid
import enum


class StatusEnum(enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    selected = "selected"
    rejected = "rejected"


class InterviewEnum(enum.Enum):
    online = "online"
    inPerson = "inPerson"


class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (db.UniqueConstraint("student_id", "drive_id"),)

    application_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    student_id = db.Column(
        db.String(36), db.ForeignKey("students.student_id"), nullable=False
    )
    drive_id = db.Column(
        db.String(36), db.ForeignKey("drives.drive_id"), nullable=False
    )
    application_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.applied)
    remarks = db.Column(db.String, nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    interview_type = db.Column(db.Enum(InterviewEnum), nullable=True)
    placement = db.relationship("Placement", backref="application", uselist=False)
