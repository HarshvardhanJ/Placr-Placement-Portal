from flask import Blueprint, json, jsonify
from app.models import company
from app.models.user import RoleEnum
from app.utils.decorators import role_required
from app.models.user import User
from app.models.student import Student
from app.models.company import Company, StatusEnum
from app.models.drive import Drive
from app.extensions import db


admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@role_required(RoleEnum.admin)
def admin_dashboard():
    return jsonify(
        {
            "total_students": Student.query.count(),
            "total_companies": Company.query.count(),
            "total_drives": Drive.query.count(),
        }
    ), 200


@admin_bp.route("/companies", methods=["GET"])
@role_required(RoleEnum.admin)
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
@role_required(RoleEnum.admin)
def approve_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    try:
        company.approval_status = StatusEnum.approved
        db.session.commit()
        return jsonify({"success": f"Company {company.name} approved"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": f"Failed to update company {id}"}), 500


@admin_bp.route("/companies/<id>/reject", methods=["PUT"])
@role_required(RoleEnum.admin)
def reject_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    try:
        company.approval_status = StatusEnum.not_approved
        db.session.commit()
        return jsonify({"success": f"Company {company.name} rejected"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": f"Failed to update company {id}"}), 500


@admin_bp.route("/companies/<id>/blacklist", methods=["PUT"])
@role_required(RoleEnum.admin)
def blacklist_company(id):
    company = Company.query.filter_by(company_id=id).first()
    if not company:
        return jsonify({"error": "Company not found!"}), 404
    user = User.query.filter_by(user_id=company.user_id).first()
    try:
        user.is_active = False
        db.session.commit()
        return jsonify({"success": f"Company {company.name} blacklisted"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": f"Failed to update company {id}"}), 500
