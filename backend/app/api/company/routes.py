from datetime import datetime
from app.extensions import db
from app.models.application import Application, ApplicationStatusEnum, InterviewEnum
from app.models.company import Company
from app.models.drive import Drive, DriveStatusEnum
from app.models.placement import Placement
from app.models.user import UserRoleEnum
from app.utils.decorators import approved_company_required, role_required
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
import os
import uuid

company_api = Blueprint("company_api", __name__)


@company_api.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.company)
@approved_company_required
def company_dashboard():
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    drives = (
        Drive.query.filter_by(company_id=company.company_id)
        .order_by(Drive.created_at.desc())
        .all()
    )

    applications = (
        Application.query.join(Drive)
        .filter(Drive.company_id == company.company_id)
        .all()
    )

    shortlisted = [
        app for app in applications if app.status == ApplicationStatusEnum.shortlisted
    ]

    selected = [
        app for app in applications if app.status == ApplicationStatusEnum.selected
    ]

    upcoming_interviews = [
        app
        for app in shortlisted
        if app.interview_date and app.interview_date > datetime.utcnow()
    ]

    return jsonify(
        {
            "company": {
                "company_id": company.company_id,
                "name": company.name,
                "industry": company.industry,
                "location": company.location,
                "description": company.description,
                "approval_status": company.approval_status.value,
            },
            "counts": {
                "drives": len(drives),
                "applications": len(applications),
                "shortlisted": len(shortlisted),
                "selected": len(selected),
                "upcoming_interviews": len(upcoming_interviews),
            },
            "recent_drives": [
                {
                    "drive_id": drive.drive_id,
                    "job_title": drive.job_title,
                    "required_skills": drive.required_skills,
                    "experience_required": drive.experience_required,
                    "benefits": drive.benefits,
                    "approval_status": drive.approval_status.value,
                    "application_deadline": str(drive.application_deadline),
                    "applications": len(drive.applications),
                }
                for drive in drives[:5]
            ],
            "recent_applications": [
                {
                    "application_id": app.application_id,
                    "student_name": app.student.name,
                    "roll_no": app.student.roll_no,
                    "job_title": app.drive.job_title,
                    "status": app.status.value,
                    "applied_on": str(app.application_date),
                }
                for app in sorted(
                    applications,
                    key=lambda a: a.application_date,
                    reverse=True,
                )[:10]
            ],
            "shortlisted_candidates": [
                {
                    "application_id": app.application_id,
                    "student_name": app.student.name,
                    "roll_no": app.student.roll_no,
                    "job_title": app.drive.job_title,
                    "interview_date": (
                        str(app.interview_date) if app.interview_date else None
                    ),
                    "interview_type": (
                        app.interview_type.value if app.interview_type else None
                    ),
                }
                for app in shortlisted[:10]
            ],
            "upcoming_interviews": [
                {
                    "application_id": app.application_id,
                    "student_name": app.student.name,
                    "job_title": app.drive.job_title,
                    "interview_date": str(app.interview_date),
                    "interview_type": (
                        app.interview_type.value if app.interview_type else None
                    ),
                }
                for app in sorted(
                    upcoming_interviews,
                    key=lambda a: a.interview_date,
                )
            ],
        }
    ), 200


@company_api.route("/profile", methods=["GET"])
@role_required(UserRoleEnum.company)
def get_company_profile():
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    return jsonify(company.to_dict()), 200


@company_api.route("/profile", methods=["PUT"])
@role_required(UserRoleEnum.company)
@approved_company_required
def update_company_profile():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    allowed_fields = {
        "contact",
        "website",
        "industry",
        "description",
        "location",
    }

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for field in data:
        if field not in allowed_fields:
            return jsonify({"message": f"Invalid field: {field}"}), 400

    try:
        company.contact = data.get("contact", company.contact)
        company.website = data.get("website", company.website)
        company.industry = data.get("industry", company.industry)
        company.description = data.get("description", company.description)
        company.location = data.get("location", company.location)
        db.session.commit()
        return jsonify(
            {
                "message": "Profile updated successfully",
                "company": company.to_dict(),
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile", "details": str(e)}), 500


@company_api.route("/drives", methods=["GET"])
@role_required(UserRoleEnum.company)
@approved_company_required
def get_company_drives():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    drives = Drive.query.filter_by(company_id=company.company_id).all()
    return jsonify({"drives": [drive.to_dict() for drive in drives]}), 200


@company_api.route("/drives", methods=["POST"])
@role_required(UserRoleEnum.company)
@approved_company_required
def create_company_drives():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    allowed_fields = {
        "job_title",
        "job_location",
        "job_description",
        "application_deadline",
        "eligible_branch",
        "min_cgpa",
        "year",
        "no_openings",
        "salary",
        "required_skills",
        "experience_required",
        "benefits",
    }

    data = request.get_json()
    if not data:
        error = {"error": "Missing data fields"}
        return jsonify(error), 400

    for field in data:
        if field not in allowed_fields:
            return jsonify({"message": f"Invalid field: {field}"}), 400

    if "job_title" not in data or "application_deadline" not in data:
        error = {"error": "Missing data fields"}
        return jsonify(error), 400

    for field in ("required_skills", "experience_required", "benefits"):
        if field in data and data[field] is not None:
            if not isinstance(data[field], str):
                return jsonify({"error": f"{field} must be text"}), 400
            if len(data[field]) > 2000:
                return jsonify({"error": f"{field} is too long"}), 400

    try:
        application_deadline = datetime.fromisoformat(data["application_deadline"])
    except ValueError:
        return jsonify({"error": "Invalid application_deadline format"}), 400
    try:
        drive = Drive(
            company_id=company.company_id,
            job_title=data["job_title"],
            job_description=data.get("job_description"),
            job_location=data.get("job_location"),
            application_deadline=application_deadline,
            eligible_branch=data.get("eligible_branch"),
            min_cgpa=data.get("min_cgpa"),
            year=data.get("year"),
            no_openings=data.get("no_openings"),
            salary=data.get("salary"),
            required_skills=data.get("required_skills"),
            experience_required=data.get("experience_required"),
            benefits=data.get("benefits"),
        )
        db.session.add(drive)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create drive", "details": str(e)}), 500

    return jsonify(
        {"message": "Drive created successfully", "drive_id": drive.drive_id}
    ), 201


@company_api.route("/drives/<id>", methods=["GET"])
@role_required(UserRoleEnum.company)
@approved_company_required
def get_drive_by_id(id):
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()
    if not drive:
        return jsonify({"error": f"Failed to find drive with id {id}"}), 404
    return jsonify(drive.to_dict()), 200


@company_api.route("/drives/<id>", methods=["PUT"])
@role_required(UserRoleEnum.company)
@approved_company_required
def update_drive(id):
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()
    if not drive:
        return jsonify({"error": f"Failed to find drive with id {id}"}), 404
    if drive.approval_status in (
        DriveStatusEnum.approved,
        DriveStatusEnum.closed,
    ):
        return jsonify({"error": "Approved or closed drives cannot be modified"}), 409

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    allowed_fields = {
        "job_title",
        "job_description",
        "job_location",
        "application_deadline",
        "eligible_branch",
        "min_cgpa",
        "year",
        "no_openings",
        "salary",
        "required_skills",
        "experience_required",
        "benefits",
    }

    for field in data:
        if field not in allowed_fields:
            return jsonify({"error": f"Field '{field}' cannot be updated"}), 400

    for field in ("required_skills", "experience_required", "benefits"):
        if field in data and data[field] is not None:
            if not isinstance(data[field], str):
                return jsonify({"error": f"{field} must be text"}), 400
            if len(data[field]) > 2000:
                return jsonify({"error": f"{field} is too long"}), 400

    try:
        if "application_deadline" in data:
            try:
                data["application_deadline"] = datetime.fromisoformat(
                    data["application_deadline"]
                )
            except ValueError:
                return jsonify({"error": "Invalid application_deadline format"}), 400

        for field in allowed_fields:
            if field in data:
                setattr(drive, field, data[field])

        db.session.commit()

        return jsonify(
            {"message": "Drive updated successfully", "drive": drive.to_dict()}
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@company_api.route("/drives/<id>/applications", methods=["GET"])
@role_required(UserRoleEnum.company)
@approved_company_required
def get_drive_application(id):
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()

    if not drive:
        return jsonify({"error": f"Failed to find drive with id {id}"}), 404

    return jsonify(
        {
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "required_skills": drive.required_skills,
            "experience_required": drive.experience_required,
            "benefits": drive.benefits,
            "applications": [
                application.to_dict() for application in drive.applications
            ],
        }
    ), 200


@company_api.route("/drives/<id>/applications/<app_id>", methods=["PUT"])
@role_required(UserRoleEnum.company)
@approved_company_required
def update_application_status(id, app_id):
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()
    if not drive:
        return jsonify({"error": f"Failed to find drive with id {id}"}), 404

    application = Application.query.filter_by(
        application_id=app_id, drive_id=id
    ).first()
    if not application:
        return jsonify({"error": f"Failed to find application with id {app_id}"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    status = data.get("status")
    remarks = data.get("remarks")

    try:
        new_status = ApplicationStatusEnum(status)
    except ValueError:
        return jsonify({"error": "Invalid status"}), 400

    if new_status == ApplicationStatusEnum.applied:
        return jsonify({"error": "Cannot change status back to applied"}), 400

    application.status = new_status
    application.remarks = remarks

    if new_status == ApplicationStatusEnum.shortlisted:
        interview_date = data.get("interview_date")
        interview_type = data.get("interview_type")

        if not interview_date or not interview_type:
            return jsonify(
                {"error": "Selected applications require interview details"}
            ), 400

        application.interview_date = datetime.fromisoformat(interview_date)
        application.interview_type = InterviewEnum(interview_type)

    if new_status == ApplicationStatusEnum.selected:
        existing_placement = Placement.query.filter_by(
            application_id=application.application_id
        ).first()

        if not existing_placement:
            placement = Placement(application_id=application.application_id)

            db.session.add(placement)
    db.session.commit()
    return jsonify(
        {
            "message": "Application updated successfully",
            "application": {
                "application_id": application.application_id,
                "status": application.status.value,
                "remarks": application.remarks,
            },
        }
    ), 200


@company_api.route("/placements", methods=["GET"])
@role_required(UserRoleEnum.company)
@approved_company_required
def get_company_placements():
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    placements = (
        Placement.query.join(Application)
        .join(Drive)
        .filter(Drive.company_id == company.company_id)
        .all()
    )

    return jsonify(
        {
            "count": len(placements),
            "placements": [
                {
                    "placement_id": placement.placement_id,
                    "student_name": placement.application.student.name,
                    "roll_no": placement.application.student.roll_no,
                    "job_title": placement.application.drive.job_title,
                    "salary": placement.salary,
                    "joining_date": (
                        str(placement.joining_date) if placement.joining_date else None
                    ),
                    "offer_letter_uploaded": bool(placement.offer_letter_path),
                    "created_at": str(placement.created_at),
                }
                for placement in placements
            ],
        }
    ), 200


@company_api.route("/placements/<placement_id>", methods=["PUT"])
@role_required(UserRoleEnum.company)
@approved_company_required
def update_placement(placement_id):
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    placement = (
        Placement.query.join(Application)
        .join(Drive)
        .filter(
            Placement.placement_id == placement_id,
            Drive.company_id == company.company_id,
        )
        .first()
    )

    if not placement:
        return jsonify({"error": "Placement not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    salary = data.get("salary")
    joining_date = data.get("joining_date")

    if salary is None:
        return jsonify({"error": "salary is required"}), 400

    if salary <= 0:
        return jsonify({"error": "salary must be greater than 0"}), 400

    if joining_date is None:
        return jsonify({"error": "joining_date is required"}), 400

    try:
        joining_date_obj = datetime.fromisoformat(joining_date)
    except ValueError:
        return jsonify(
            {
                "error": (
                    "Invalid joining_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
            }
        ), 400

    try:
        placement.salary = salary
        placement.joining_date = joining_date_obj

        db.session.commit()

        return jsonify(
            {
                "message": "Placement updated successfully",
                "placement": {
                    "placement_id": placement.placement_id,
                    "application_id": placement.application_id,
                    "student_name": placement.application.student.name,
                    "job_title": placement.application.drive.job_title,
                    "salary": placement.salary,
                    "joining_date": str(placement.joining_date),
                    "offer_letter_uploaded": (placement.offer_letter_path is not None),
                    "created_at": str(placement.created_at),
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "error": "Failed to update placement",
                "details": str(e),
            }
        ), 500


@company_api.route("/placements/<placement_id>/offer-letter", methods=["POST"])
@role_required(UserRoleEnum.company)
@approved_company_required
def upload_offer_letter(placement_id):
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    placement = (
        Placement.query.join(Application)
        .join(Drive)
        .filter(
            Placement.placement_id == placement_id,
            Drive.company_id == company.company_id,
        )
        .first()
    )

    if not placement:
        return jsonify({"error": "Placement not found"}), 404

    offer_letter = request.files.get("offer_letter")

    if not offer_letter:
        return jsonify({"error": "Offer letter file is required"}), 400

    if not offer_letter.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    filepath = None

    try:
        old_offer_letter_path = placement.offer_letter_path

        unique_filename = f"{placement.placement_id}_{uuid.uuid4()}.pdf"

        upload_folder = os.path.join(
            os.getcwd(),
            "uploads",
            "offer_letters",
        )

        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(
            upload_folder,
            unique_filename,
        )

        offer_letter.save(filepath)

        placement.offer_letter_path = filepath

        db.session.commit()

        if (
            old_offer_letter_path
            and old_offer_letter_path != filepath
            and os.path.exists(old_offer_letter_path)
        ):
            os.remove(old_offer_letter_path)

        return jsonify(
            {
                "message": "Offer letter uploaded successfully",
                "placement_id": placement.placement_id,
                "offer_letter_path": filepath,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        if filepath and os.path.exists(filepath):
            os.remove(filepath)

        return jsonify(
            {
                "error": "Failed to upload offer letter",
                "details": str(e),
            }
        ), 500


@company_api.route("/drives/<id>/close", methods=["PUT"])
@role_required(UserRoleEnum.company)
@approved_company_required
def close_drive(id):
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    if drive.approval_status == DriveStatusEnum.closed:
        return jsonify({"error": "Drive is already closed"}), 409

    try:
        drive.approval_status = DriveStatusEnum.closed
        db.session.commit()

        return jsonify(
            {
                "message": "Drive closed successfully",
                "drive_id": drive.drive_id,
                "status": drive.approval_status.value,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "error": "Failed to close drive",
                "details": str(e),
            }
        ), 500
