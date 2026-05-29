from app.extensions import db
import uuid
import enum


class StatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    closed = "closed"


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
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    job_title = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String, nullable=True)
    job_location = db.Column(db.String, nullable=True, default="NA")
    application_deadline = db.Column(db.DateTime, nullable=False)
    eligible_branch = db.Column(db.String, nullable=True)
    min_cgpa = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    no_openings = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    applications = db.relationship("Application", backref="drive", lazy=True)
