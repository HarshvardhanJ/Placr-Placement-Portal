from app.extensions import db
import uuid


class Placement(db.Model):
    __tablename__ = "placements"

    placement_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    application_id = db.Column(
        db.String(36),
        db.ForeignKey("applications.application_id"),
        nullable=False,
        unique=True,
    )
    offer_letter_path = db.Column(db.String, nullable=True)
    joining_date = db.Column(db.DateTime, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
