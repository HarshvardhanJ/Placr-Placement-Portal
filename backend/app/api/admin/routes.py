from flask import Blueprint, json, jsonify
from app.models import company
from app.models import drive
from app.models.user import UserRoleEnum
from app.utils.decorators import role_required
from app.models.user import User
from app.models.student import Student
from app.models.company import Company, CompanyStatusEnum
from app.models.drive import Drive, DriveStatusEnum
from app.extensions import db


admin_bp = Blueprint("admin_bp", __name__)


# ADMIN DASHBOARD
@admin_bp.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_dashboard():
    return jsonify(
        {
            "total_students": Student.query.count(),
            "total_companies": Company.query.count(),
            "total_drives": Drive.query.count(),
        }
    ), 200


# ADMIN - COMPANY ROUTES
@admin_bp.route("/companies", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_companies():
    companies = Company.query.all()
    result = []
    for c in companies:
        user = User.query.filter_by(user_id=c.user_id).first()
        data = c.to_dict()
        data["is_active"] = user.is_active
        result.append(data)
    return jsonify(result), 200


@admin_bp.route("/companies/<id>/approve", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def approve_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    try:
        company.approval_status = CompanyStatusEnum.approved
        db.session.commit()
        return jsonify({"success": f"Company {company.name} approved"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update company {id}", "details": str(e)}
        ), 500


@admin_bp.route("/companies/<id>/reject", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def reject_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    try:
        company.approval_status = CompanyStatusEnum.not_approved
        db.session.commit()
        return jsonify({"success": f"Company {company.name} rejected"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update company {id}", "details": str(e)}
        ), 500


@admin_bp.route("/companies/<id>/blacklist", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def blacklist_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    user = User.query.filter_by(user_id=company.user_id).first()
    try:
        user.is_active = False
        db.session.commit()
        return jsonify({"success": f"Company {company.name} blacklisted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update company {id}", "details": str(e)}
        ), 500


# ADMIN - STUDENT ROUTES
@admin_bp.route("/students", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_students():
    students = Student.query.all()
    result = []
    for s in students:
        user = User.query.filter_by(user_id=s.user_id).first()
        data = s.to_dict()
        data["is_active"] = user.is_active
        result.append(data)
    return jsonify(result), 200


@admin_bp.route("/students/<id>/blacklist", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def blacklist_student(id):
    student = Student.query.filter_by(student_id=id).first()
    if not student:
        return jsonify({"error": "Student not found!"}), 404
    user = User.query.filter_by(user_id=student.user_id).first()
    try:
        user.is_active = False
        db.session.commit()
        return jsonify({"success": f"Student {student.name} blacklisted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update student {id}", "details": str(e)}
        ), 500


# ADMIN - DRIVES ROUTES
@admin_bp.route("/drives", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_drives():
    drives = Drive.query.all()
    return jsonify([d.to_dict() for d in drives]), 200


@admin_bp.route("/drives/<id>/approve", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def approve_drives(id):
    drive = Drive.query.filter_by(drive_id=id).first()
    if not drive:
        return jsonify({"error": "Drive not found!"}), 404
    try:
        drive.approval_status = DriveStatusEnum.approved
        db.session.commit()
        return jsonify({"success": f"Drive {id} approved"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update drive {id}", "details": str(e)}
        ), 500


@admin_bp.route("/drives/<id>/reject", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def reject_drives(id):
    drive = Drive.query.filter_by(drive_id=id).first()
    if not drive:
        return jsonify({"error": "Drive not found!"}), 404
    try:
        drive.approval_status = DriveStatusEnum.rejected
        db.session.commit()
        return jsonify({"success": f"Drive {id} rejected"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update drive {id}", "details": str(e)}
        ), 500
