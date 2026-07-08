from datetime import datetime
import uuid
from flask import Blueprint, json, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
import os
from app.extensions import db
from app.models.application import Application, ApplicationStatusEnum
from app.models.drive import Drive, DriveStatusEnum
from app.models.student import Student
from app.models.user import User, UserRoleEnum
from app.models.company import Company
from app.models.placement import Placement
from app.utils.decorators import active_required, role_required


student_api = Blueprint("student_api", __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
RESUME_UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")


def _get_resume_path(student):
    if not student.resume_path:
        return None
    return student.resume_path


def normalize_branch_list(value):
    if not value:
        return ["ALL"]

    raw = str(value).replace(";", ",").replace("/", ",")
    branches = [part.strip().upper() for part in raw.split(",") if part.strip()]

    return branches or ["ALL"]


def student_is_eligible_for_drive(student, drive):
    if drive.approval_status != DriveStatusEnum.approved:
        return False

    if drive.application_deadline <= datetime.utcnow():
        return False

    if drive.min_cgpa is not None and student.cgpa is not None:
        if float(student.cgpa) < float(drive.min_cgpa):
            return False

    if drive.year is not None and student.year is not None:
        if int(student.year) != int(drive.year):
            return False

    student_branch = (student.department or "").strip().upper()
    branches = normalize_branch_list(drive.eligible_branch)

    return "ALL" in branches or student_branch in branches


@student_api.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
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
        if (
            student_is_eligible_for_drive(student, drive)
            and drive.drive_id not in applied_drive_ids
        ):
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


@student_api.route("/profile", methods=["GET"])
@role_required(UserRoleEnum.student)
def get_student_profile():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


@student_api.route("/profile", methods=["PUT"])
@role_required(UserRoleEnum.student)
@active_required
def set_student_profile():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    allowed_fields = {
        "name",
        "department",
        "cgpa",
        "year",
        "phone_number",
        "skills",
        "experience",
    }

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for field in data:
        if field not in allowed_fields:
            return jsonify({"error": f"Field '{field}' cannot be updated"}), 400

    if "cgpa" in data:
        if not (0 <= data["cgpa"] <= 10):
            return jsonify({"error": "CGPA must be between 0 and 10"}), 400

    if "year" in data:
        if data["year"] not in [1, 2, 3, 4]:
            return jsonify({"error": "Year must be between 1 and 4"}), 400

    for field in ("skills", "experience"):
        if field in data and data[field] is not None:
            if not isinstance(data[field], str):
                return jsonify({"error": f"{field} must be text"}), 400
            if len(data[field]) > 2000:
                return jsonify({"error": f"{field} is too long"}), 400

    try:
        student.name = data.get("name", student.name)
        student.department = data.get("department", student.department)
        student.cgpa = data.get("cgpa", student.cgpa)
        student.year = data.get("year", student.year)
        student.phone_number = data.get("phone_number", student.phone_number)
        student.skills = data.get("skills", student.skills)
        student.experience = data.get("experience", student.experience)
        db.session.commit()
        return jsonify(
            {
                "message": "Profile updated successfully",
                "student": student.to_dict(),
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile", "details": str(e)}), 500


@student_api.route("/profile/resume", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def get_resume():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    resume_path = _get_resume_path(student)
    if not resume_path:
        return jsonify({"error": "Resume not uploaded"}), 404

    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file missing"}), 404

    return send_file(
        resume_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"{student.roll_no}_resume.pdf",
    )


@student_api.route("/profile/resume", methods=["POST"])
@role_required(UserRoleEnum.student)
@active_required
def upload_resume():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    resume = request.files.get("resume")
    if not resume:
        return jsonify({"error": "Resume file is required"}), 400
    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    filepath = None
    try:
        old_resume_path = student.resume_path
        unique_filename = f"{student.student_id}_{uuid.uuid4()}.pdf"

        os.makedirs(RESUME_UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(RESUME_UPLOAD_FOLDER, unique_filename)
        resume.save(filepath)

        student.resume_path = filepath
        db.session.commit()
        if (
            old_resume_path
            and old_resume_path != filepath
            and os.path.exists(old_resume_path)
        ):
            os.remove(old_resume_path)
        return jsonify(
            {
                "message": "Resume uploaded successfully",
                "resume_path": filepath,
                "resume_uploaded": True,
                "resume_filename": os.path.basename(filepath),
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({"error": "Failed to upload file", "details": str(e)}), 500


@student_api.route("/drives/<id>", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def get_drive_details(id):
    drive = Drive.query.filter_by(
        drive_id=id, approval_status=DriveStatusEnum.approved
    ).first()
    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    return jsonify(drive.to_dict()), 200


@student_api.route("/drives/<id>/apply", methods=["POST"])
@role_required(UserRoleEnum.student)
@active_required
def student_apply(id):
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    drive = Drive.query.filter_by(
        drive_id=id, approval_status=DriveStatusEnum.approved
    ).first()
    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if student.department is None or student.cgpa is None or student.year is None:
        return jsonify({"error": "Complete your profile before applying"}), 400

    if not student.resume_path:
        return jsonify({"error": "Upload your resume before applying"}), 400

    if drive.application_deadline < datetime.utcnow():
        return jsonify({"error": "Application deadline has passed"}), 400

    if drive.min_cgpa is not None and student.cgpa < drive.min_cgpa:
        return jsonify({"error": f"Minimum CGPA required is {drive.min_cgpa}"}), 403

    if drive.year is not None and student.year != drive.year:
        return jsonify({"error": f"Only year {drive.year} students can apply"}), 403

    if not student_is_eligible_for_drive(student, drive):
        return jsonify({"error": "You are not eligible for this drive"}), 403

    existing_application = Application.query.filter_by(
        student_id=student.student_id,
        drive_id=drive.drive_id,
    ).first()

    if existing_application:
        return jsonify({"error": "You have already applied to this drive"}), 409

    try:
        application = Application(
            student_id=student.student_id,
            drive_id=drive.drive_id,
        )

        db.session.add(application)
        db.session.commit()

        return jsonify(
            {
                "message": "Application submitted successfully",
                "application_id": application.application_id,
            }
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "error": "Failed to submit application",
                "details": str(e),
            }
        ), 500


@student_api.route("/applications", methods=["GET"])
@role_required(UserRoleEnum.student)
def get_student_applications():
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    applications = Application.query.filter_by(student_id=student.student_id).all()

    return jsonify(
        {
            "count": len(applications),
            "applications": [app.to_dict() for app in applications],
        }
    ), 200


@student_api.route("/drives", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def get_available_drives():
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if student.department is None or student.cgpa is None or student.year is None:
        return jsonify(
            {
                "error": (
                    "Complete your profile "
                    "(department, CGPA, year) before viewing drives"
                )
            }
        ), 400

    search = request.args.get("search", "").strip()

    applied_drive_ids = {
        app.drive_id
        for app in Application.query.filter_by(student_id=student.student_id).all()
    }

    query = Drive.query.join(Company).filter(
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
    )

    if search:
        query = query.filter(
            db.or_(
                Company.name.ilike(f"%{search}%"),
                Drive.job_title.ilike(f"%{search}%"),
                Drive.job_description.ilike(f"%{search}%"),
                Drive.required_skills.ilike(f"%{search}%"),
            )
        )

    drives = query.all()

    eligible_drives = []
    for drive in drives:
        if (
            student_is_eligible_for_drive(student, drive)
            and drive.drive_id not in applied_drive_ids
        ):
            eligible_drives.append(drive)

    eligible_drives.sort(key=lambda drive: drive.application_deadline)

    return jsonify(
        {
            "count": len(eligible_drives),
            "drives": [drive.to_dict() for drive in eligible_drives],
        }
    ), 200


@student_api.route("/placements", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def get_student_placements():
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    placements = (
        Placement.query.join(Application)
        .filter(Application.student_id == student.student_id)
        .all()
    )

    return jsonify(
        {
            "count": len(placements),
            "placements": [
                {
                    "placement_id": placement.placement_id,
                    "company": (placement.application.drive.company.name),
                    "job_title": (placement.application.drive.job_title),
                    "salary": placement.salary,
                    "joining_date": (
                        str(placement.joining_date) if placement.joining_date else None
                    ),
                    "offer_letter_available": (placement.offer_letter_path is not None),
                    "created_at": str(placement.created_at),
                }
                for placement in placements
            ],
        }
    ), 200


@student_api.route("/placements/<placement_id>", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def get_placement_details(placement_id):
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    placement = (
        Placement.query.join(Application)
        .filter(
            Placement.placement_id == placement_id,
            Application.student_id == student.student_id,
        )
        .first()
    )

    if not placement:
        return jsonify({"error": "Placement not found"}), 404

    return jsonify(
        {
            "placement_id": placement.placement_id,
            "company": placement.application.drive.company.name,
            "job_title": placement.application.drive.job_title,
            "salary": placement.salary,
            "joining_date": (
                str(placement.joining_date) if placement.joining_date else None
            ),
            "offer_letter_available": bool(placement.offer_letter_path),
            "created_at": str(placement.created_at),
        }
    ), 200


@student_api.route("/placements/<placement_id>/offer-letter", methods=["GET"])
@role_required(UserRoleEnum.student)
@active_required
def download_offer_letter(placement_id):
    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    placement = (
        Placement.query.join(Application)
        .filter(
            Placement.placement_id == placement_id,
            Application.student_id == student.student_id,
        )
        .first()
    )

    if not placement:
        return jsonify({"error": "Placement not found"}), 404

    if not placement.offer_letter_path:
        return jsonify({"error": "Offer letter not available"}), 404

    if not os.path.exists(placement.offer_letter_path):
        return jsonify({"error": "Offer letter file missing"}), 404

    return send_file(
        placement.offer_letter_path,
        as_attachment=True,
        download_name=f"offer_letter_{student.name}.pdf",
        mimetype="application/pdf",
    )


@student_api.route("/exports", methods=["POST"])
@role_required(UserRoleEnum.student)
def trigger_student_export():
    from app.jobs.exports import export_student_history

    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "Unauthorized"}), 403

    if not user.student_profile:
        return jsonify({"error": "Student profile not found"}), 404

    task = export_student_history.delay(user_id, user.email)
    return jsonify(
        {
            "message": "Export started. You will receive an email when it is ready.",
            "task_id": task.id,
        }
    ), 202


@student_api.route("/exports/status/<task_id>", methods=["GET"])
@role_required(UserRoleEnum.student)
def export_status(task_id):
    from app.jobs.exports import export_student_history

    result = export_student_history.AsyncResult(task_id)
    return jsonify(
        {
            "task_id": task_id,
            "state": result.state,
            "result": result.result if result.ready() else None,
        }
    )


@student_api.route("/exports/download/<path:filename>", methods=["GET"])
@role_required(UserRoleEnum.student)
def download_export(filename):
    from app.jobs.exports import _get_export_dir

    export_folder = _get_export_dir()

    safe_root = os.path.abspath(export_folder)
    filepath = os.path.abspath(os.path.join(export_folder, filename))
    if not filepath.startswith(safe_root + os.sep):
        return jsonify({"error": "Invalid file path"}), 400
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_file(filepath, as_attachment=True, download_name=filename)
