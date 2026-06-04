from datetime import datetime
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.application import Application, ApplicationStatusEnum
from app.models.drive import Drive, DriveStatusEnum
from app.models.student import Student
from app.models.user import UserRoleEnum
from app.utils.decorators import role_required

student_api = Blueprint("student_api", __name__)


@student_api.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.student)
def student_dashboard():
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if student.department is None or student.cgpa is None or student.year is None:
        return jsonify(
            {
                "error": (
                    "Complete your profile "
                    "(department, CGPA, year) before viewing eligible drives"
                )
            }
        ), 400

    applications = Application.query.filter_by(student_id=student.student_id).all()

    applied_drive_ids = {app.drive_id for app in applications}

    open_drives = Drive.query.filter(
        Drive.approval_status == DriveStatusEnum.approved,
        Drive.application_deadline > datetime.utcnow(),
        db.or_(
            Drive.min_cgpa == None,
            Drive.min_cgpa <= student.cgpa,
        ),
        db.or_(
            Drive.year == None,
            Drive.year == student.year,
        ),
    ).all()

    eligible_drives = []

    for drive in open_drives:
        branches = [
            branch.strip() for branch in (drive.eligible_branch or "").split(",")
        ]

        if (
            "ALL" in branches or student.department in branches
        ) and drive.drive_id not in applied_drive_ids:
            eligible_drives.append(drive)

    eligible_drives.sort(key=lambda drive: drive.application_deadline)

    applied = [
        app for app in applications if app.status == ApplicationStatusEnum.applied
    ]

    shortlisted = [
        app for app in applications if app.status == ApplicationStatusEnum.shortlisted
    ]

    selected = [
        app for app in applications if app.status == ApplicationStatusEnum.selected
    ]

    upcoming_interviews = sorted(
        [
            {
                "application_id": app.application_id,
                "company": app.drive.company.name,
                "job_title": app.drive.job_title,
                "interview_date": str(app.interview_date),
                "interview_type": (
                    app.interview_type.value if app.interview_type else None
                ),
            }
            for app in applications
            if (app.interview_date and app.interview_date > datetime.utcnow())
        ],
        key=lambda interview: interview["interview_date"],
    )

    return jsonify(
        {
            "counts": {
                "eligible": len(eligible_drives),
                "applied": len(applied),
                "shortlisted": len(shortlisted),
                "selected": len(selected),
            },
            "eligible_drives": [
                {
                    **drive.to_dict(),
                    "status": "eligible",
                }
                for drive in eligible_drives
            ],
            "applied_drives": [
                {
                    "application_id": app.application_id,
                    "application_date": str(app.application_date),
                    "status": "applied",
                    "drive": app.drive.to_dict(),
                }
                for app in applied
            ],
            "shortlisted_drives": [
                {
                    "application_id": app.application_id,
                    "status": "shortlisted",
                    "remarks": app.remarks,
                    "interview_date": (
                        str(app.interview_date) if app.interview_date else None
                    ),
                    "interview_type": (
                        app.interview_type.value if app.interview_type else None
                    ),
                    "drive": app.drive.to_dict(),
                }
                for app in shortlisted
            ],
            "selected_drives": [
                {
                    "application_id": app.application_id,
                    "status": "selected",
                    "remarks": app.remarks,
                    "interview_date": (
                        str(app.interview_date) if app.interview_date else None
                    ),
                    "interview_type": (
                        app.interview_type.value if app.interview_type else None
                    ),
                    "drive": app.drive.to_dict(),
                }
                for app in selected
            ],
            "upcoming_interviews": upcoming_interviews,
        }
    ), 200
