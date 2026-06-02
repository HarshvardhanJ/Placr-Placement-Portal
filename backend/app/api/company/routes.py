from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models import company
from app.models import application
from app.models.application import Application
from app.models.company import Company
from app.models.application import Application, ApplicationStatusEnum
from app.models.company import Company
from app.models.drive import Drive, DriveStatusEnum
from app.utils.decorators import role_required
from app.models.user import UserRoleEnum
from app.extensions import db


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
    selected_count = {
        Application.query.join(Drive)
        .filter(
            Drive.company_id == company.company_id,
            Application.status == ApplicationStatusEnum.selected,
        )
        .count()
    }
    application_count = {
        Application.query.join(Drive)
        .filter(Drive.company_id == company.company_id)
        .count()
    }
    if not drive_count or selected_count or application_count:
        return jsonify({"error": "Data not found"}), 404

    return jsonify(
        {
            "company": {
                "name": company.name,
                "company_id": company.company_id,
                "description": company.description,
                "industry": company.industry,
                "location": company.location,
                "approval_status": company.approval_status,
            },
            "status": {
                "total_drives": company.drive_count,
                "total_applications": application_count,
                "total_selected": selected_count,
            },
        }
    ), 200


@company_api.route("/profile")
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

    for field in data:
    if field not in allowed_fields:
        return jsonify(
            {"message": f"Invalid field: {field}"}
        ), 400
    
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
    except Exception:
        db.session.rollback()
        return jsonify({"error": f"Failed to update profile"}), 500


@company_api.route("/drives")
@role_required(UserRoleEnum.company)
def get_company_drives():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    drives = Drive.query.filter_by(company_id=company.company_id).all()
    return jsonify({[drive.to_dict() for drive in drives]}), 200


@company_api.route("/drives", method=["POST"])
@role_required(UserRoleEnum.company)
def create_company_drives():
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    
    if not company:
        return jsonify({"error": "Company not found"}), 404

    allowed_fields = {
        "company_id",
        "job_title",
        "job_location",
        "job_description",
        "application_deadline",
        "eligible_branch",
        "min_cgpa",
        "year",
        "no_openings",
        "salary"
    }

    data = request.get_json()

    for field in data:
        if field not in allowed_fields:
            return jsonify(
                {"message": f"Invalid field: {field}"}
            ), 400
    
    if (
            not data
            or "company_id" not in data 
            or "job_title" not in data 
            or "application_deadline" not in data
    ):
        error = {"error": "Missing data fields"}
        return jsonify(error), 400

    try:
        drive = Drive(company_id=company.company_id, job_title=data["job_title"], application_deadline=data["application_deadline"])
        db.session.add(drive)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error":"Failed to create drive"}), 500

    return jsonify({"success" : "Drive created successfully"}), 200



