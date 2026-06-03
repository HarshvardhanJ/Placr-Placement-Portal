from app.extensions import db
import uuid
import enum


class ApplicationStatusEnum(enum.Enum):
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
    status = db.Column(
        db.Enum(ApplicationStatusEnum),
        nullable=False,
        default=ApplicationStatusEnum.applied,
    )
    remarks = db.Column(db.String, nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    interview_type = db.Column(db.Enum(InterviewEnum), nullable=True)
    placement = db.relationship("Placement", backref="application", uselist=False)

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "student_id": self.student_id,
            "application_date": str(self.application_date),
            "status": self.status.value,
            "remarks": self.remarks,
            "interview_date": str(self.interview_date)
            if self.status == ApplicationStatusEnum.shortlisted
            else "NA",
            "interview_type": self.interview_type.value
            if self.status == ApplicationStatusEnum.shortlisted
            else "NA",
        }
