from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.application import Application, ApplicationStatusEnum, InterviewEnum
from app.models.company import Company
from app.models.drive import Drive, DriveStatusEnum
from app.models.placement import Placement
from app.utils.decorators import approved_company_required, role_required
from app.models.user import UserRoleEnum
from app.extensions import db
from datetime import datetime


company_api = Blueprint("company_api", __name__)


@company_api.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.company)
def company_dashboard():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    drives = Drive.query.filter_by(company_id=company.company_id)
    drive_count = drives.count()
    selected_count = (
        Application.query.join(Drive)
        .filter(
            Drive.company_id == company.company_id,
            Application.status == ApplicationStatusEnum.selected,
        )
        .count()
    )
    application_count = (
        Application.query.join(Drive)
        .filter(Drive.company_id == company.company_id)
        .count()
    )

    return jsonify(
        {
            "company": {
                "name": company.name,
                "company_id": company.company_id,
                "description": company.description,
                "industry": company.industry,
                "location": company.location,
                "approval_status": company.approval_status.value,
            },
            "status": {
                "total_drives": drive_count,
                "total_applications": application_count,
                "total_selected": selected_count,
            },
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
    }

    data = request.get_json()

    for field in data:
        if field not in allowed_fields:
            return jsonify({"message": f"Invalid field: {field}"}), 400

    if not data or "job_title" not in data or "application_deadline" not in data:
        error = {"error": "Missing data fields"}
        return jsonify(error), 400
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
    }

    for field in data:
        if field not in allowed_fields:
            return jsonify({"error": f"Field '{field}' cannot be updated"}), 400

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

    if new_status == ApplicationStatusEnum.selected:
        interview_date = data.get("interview_date")
        interview_type = data.get("interview_type")

        if not interview_date or not interview_type:
            return jsonify(
                {"error": "Selected applications require interview details"}
            ), 400

        application.interview_date = datetime.fromisoformat(interview_date)
        application.interview_type = InterviewEnum(interview_type)

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


@company_api.route(
    "/drives/<string:id>/applications/<string:app_id>/placement", methods=["POST"]
)
@role_required(UserRoleEnum.company)
def create_placement(id, app_id):
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404

    drive = Drive.query.filter_by(drive_id=id, company_id=company.company_id).first()

    if not drive:
        return jsonify({"error": f"Failed to find drive with id {id}"}), 404

    application = Application.query.filter_by(
        application_id=app_id, drive_id=drive.drive_id
    ).first()

    if not application:
        return jsonify({"error": f"Failed to find application with id {app_id}"}), 404

    if application.status != ApplicationStatusEnum.selected:
        return jsonify({"error": "Only selected applications can be placed"}), 400

    if application.placement:
        return jsonify({"error": "Placement already exists for this application"}), 409

    data = request.get_json()

    salary = data.get("salary")
    try:
        joining_date_obj = datetime.fromisoformat(joining_date)
    except ValueError:
        return jsonify({"error": "Invalid joining_date format"}), 400
    offer_letter_path = data.get("offer_letter_path")

    if salary is None:
        return jsonify({"error": "salary is required"}), 400

    if joining_date is None:
        return jsonify({"error": "joining_date is required"}), 400

    try:
        placement = Placement(
            application_id=application.application_id,
            salary=salary,
            joining_date=joining_date_obj,
            offer_letter_path=offer_letter_path,
        )

        db.session.add(placement)
        db.session.commit()

        return jsonify(
            {
                "message": "Placement created successfully",
                "placement": {
                    "placement_id": placement.placement_id,
                    "application_id": placement.application_id,
                    "salary": placement.salary,
                    "joining_date": str(placement.joining_date),
                    "offer_letter_path": placement.offer_letter_path,
                    "created_at": str(placement.created_at),
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
