from app.extensions import db
import uuid
import enum


class DriveStatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    closed = "closed"
    rejected = "rejected"


class Drive(db.Model):
    __tablename__ = "drives"
    __table_args__ = (
        db.CheckConstraint("min_cgpa >= 0 AND min_cgpa <= 10"),
        db.CheckConstraint("no_openings > 0"),
    )

    drive_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    company_id = db.Column(
        db.String(36), db.ForeignKey("companies.company_id"), nullable=False
    )
    approval_status = db.Column(
        db.Enum(DriveStatusEnum), nullable=False, default=DriveStatusEnum.pending
    )
    job_title = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String, nullable=True)
    job_location = db.Column(db.String, nullable=True, default="NA")
    application_deadline = db.Column(db.DateTime, nullable=False)
    eligible_branch = db.Column(db.String, nullable=True)
    min_cgpa = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    no_openings = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    required_skills = db.Column(db.Text, nullable=True)
    experience_required = db.Column(db.String, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    applications = db.relationship("Application", backref="drive", lazy=True)

    def to_dict(self):
        return {
            "company_name": self.company.name,
            "drive_id": self.drive_id,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "job_location": self.job_location,
            "application_deadline": str(self.application_deadline),
            "min_cgpa": self.min_cgpa,
            "required_skills": self.required_skills,
            "experience_required": self.experience_required,
            "benefits": self.benefits,
            "approval_status": self.approval_status.value,
            "year": self.year,
            "no_openings": self.no_openings,
            "salary": self.salary,
            "created_at": str(self.created_at),
        }
