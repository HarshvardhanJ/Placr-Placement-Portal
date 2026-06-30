from flask import Blueprint, jsonify, request
from app.models.user import UserRoleEnum
from app.utils.decorators import role_required
from app.models.user import User
from app.models.student import Student
from app.models.company import Company, CompanyStatusEnum
from app.models.drive import Drive, DriveStatusEnum
from app.extensions import db
from app.models.application import Application


admin_bp = Blueprint("admin_bp", __name__)


# ADMIN DASHBOARD
@admin_bp.route("/dashboard", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_dashboard():

    pending_companies = (
        Company.query.filter(Company.approval_status == CompanyStatusEnum.not_approved)
        .limit(5)
        .all()
    )

    pending_drives = (
        Drive.query.filter(Drive.approval_status == DriveStatusEnum.pending)
        .limit(5)
        .all()
    )

    recent_companies = Company.query.order_by(Company.created_at.desc()).limit(3).all()

    recent_drives = Drive.query.order_by(Drive.created_at.desc()).limit(3).all()

    return jsonify(
        {
            "stats": {
                "students": Student.query.count(),
                "companies": Company.query.count(),
                "drives": Drive.query.count(),
                "applications": Application.query.count(),
                "pending_companies": Company.query.filter(
                    Company.approval_status == CompanyStatusEnum.not_approved
                ).count(),
                "pending_drives": Drive.query.filter(
                    Drive.approval_status == DriveStatusEnum.pending
                ).count(),
                "blacklisted": User.query.filter(User.is_active == False).count(),
            },
            "pending": (
                [
                    {
                        "title": c.name,
                        "subtitle": "Company Approval",
                        "link": "/admin/companies",
                    }
                    for c in pending_companies
                ]
                + [
                    {
                        "title": d.job_title,
                        "subtitle": "Drive Approval",
                        "link": "/admin/drives",
                    }
                    for d in pending_drives
                ]
            ),
            "recent_activity": (
                [
                    {
                        "message": f"{c.name} registered",
                        "time": c.created_at.isoformat(),
                    }
                    for c in recent_companies
                ]
                + [
                    {
                        "message": f"{d.job_title} drive created",
                        "time": d.created_at.isoformat(),
                    }
                    for d in recent_drives
                ]
            ),
            "recent_drives": [
                {
                    "drive_id": d.drive_id,
                    "company_name": d.company.name,
                    "job_location": d.job_location,
                    "job_title": d.job_title,
                    "application_deadline": str(
                        d.application_deadline.strftime("%d %b %Y")
                    ),
                    "applicants": len(d.applications),
                    "approval_status": d.approval_status.value,
                }
                for d in recent_drives
            ],
        }
    ), 200


# ADMIN - COMPANY ROUTES
@admin_bp.route("/companies", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_companies():
    search = request.args.get("search", "")
    query = Company.query

    search = search.strip() if search else search
    if search:
        query = query.filter(
            db.or_(
                Company.name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%"),
            )
        )

    companies = query.all()
    result = []
    for c in companies:
        user = User.query.filter_by(user_id=c.user_id).first()
        data = c.to_dict()
        data["is_active"] = user.is_active
        data["drives"] = len(c.drives)
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
    search = request.args.get("search", "")
    query = Student.query

    search = search.strip() if search else search
    if search:
        query = query.filter(
            db.or_(
                Student.name.ilike(f"%{search}%"),
                Student.roll_no.ilike(f"%{search}%"),
                Student.phone_number.ilike(f"%{search}%"),
            )
        )

    students = query.all()
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
    drives = Drive.query.order_by(Drive.created_at.desc()).all()

    return jsonify(
        [
            {
                **d.to_dict(),
                "applicants": len(d.applications),
            }
            for d in drives
        ]
    )


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


@admin_bp.route("/drives/<id>/close", methods=["PUT"])
@role_required(UserRoleEnum.admin)
def close_drive(id):
    drive = Drive.query.filter_by(drive_id=id).first()

    if not drive:
        return jsonify({"error": "Drive not found"}), 404
    try:
        drive.approval_status = DriveStatusEnum.closed
        db.session.commit()
        return jsonify({"success": "Drive closed"})
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"Failed to update drive {id}", "details": str(e)}
        ), 500


@admin_bp.route("/applications", methods=["GET"])
@role_required(UserRoleEnum.admin)
def admin_applications():
    applications = Application.query.all()

    return jsonify(
        [
            {
                "application_id": app.application_id,
                "student_name": app.student.name,
                "roll_no": app.student.roll_no,
                "company": app.drive.company.name,
                "job_title": app.drive.job_title,
                "status": app.status.value,
                "application_date": str(app.application_date),
            }
            for app in applications
        ]
    ), 200
