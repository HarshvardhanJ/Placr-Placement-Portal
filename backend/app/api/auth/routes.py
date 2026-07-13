from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.extensions import bcrypt, db
from app.models.company import Company
from app.models.student import Student
from app.models.user import User, UserRoleEnum
from app.utils.cache_helper import clear_cache_pattern
import re

auth_bp = Blueprint("auth_bp", __name__)
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data or "email" not in data or "password" not in data:
        error = {"error": "Missing email or password in request body"}
        return jsonify(error), 400

    email = normalize_text(data.get("email")).lower()
    password = data["password"]

    if not validate_email(email):
        return jsonify({"error": "Enter a valid email address"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User does not exist"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        error = {"error": "Wrong email or password!"}
        return jsonify(error), 401

    if not user.is_active:
        return jsonify(
            {
                "error": "Your account has been deactivated. Please contact the administrator."
            }
        ), 403

    token = create_access_token(identity=user.user_id)
    return jsonify(
        {"token": token, "user": {"email": user.email, "role": user.role.value}}
    ), 200


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json(silent=True)

    if (
        not data
        or "email" not in data
        or "password" not in data
        or "repeat_password" not in data
        or "name" not in data
        or "roll_no" not in data
    ):
        error = {"error": "Missing data fields"}
        return jsonify(error), 400

    email = normalize_text(data["email"]).lower()
    password = data["password"]
    repeat_password = data["repeat_password"]
    name = normalize_text(data["name"])
    roll_no = normalize_text(data["roll_no"])
    role = UserRoleEnum.student

    if not validate_email(email):
        return jsonify({"error": "Enter a valid email address"}), 400
    if len(name) < 2:
        return jsonify({"error": "Full name must be at least 2 characters"}), 400
    if not roll_no:
        return jsonify({"error": "Roll number is required"}), 400

    if User.query.filter_by(email=email).first():
        error = {"error": "User already exists"}
        return jsonify(error), 409

    if not validate_password(password):
        return {
            "error": (
                "Password must be at least 8 characters long "
                "and contain uppercase, lowercase, and numeric characters."
            )
        }, 400

    if password != repeat_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if Student.query.filter_by(roll_no=roll_no).first():
        return jsonify({"error": "Student with this roll number already exists"}), 409
    hashed_pass = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        user = User(email=email, password=hashed_pass, role=role)
        db.session.add(user)
        db.session.flush()

        student = Student(user_id=user.user_id, name=name, roll_no=roll_no)
        db.session.add(student)
        db.session.commit()
        clear_cache_pattern("admin_")
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

    return jsonify({"success": "User created successfully!"}), 201


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json(silent=True)

    if (
        not data
        or "email" not in data
        or "password" not in data
        or "repeat_password" not in data
        or "name" not in data
    ):
        error = {"error": "Missing data fields"}
        return jsonify(error), 400

    email = normalize_text(data["email"]).lower()
    password = data["password"]
    repeat_password = data["repeat_password"]
    name = normalize_text(data["name"])
    role = UserRoleEnum.company

    if not validate_email(email):
        return jsonify({"error": "Enter a valid email address"}), 400
    if len(name) < 2:
        return jsonify({"error": "Company name must be at least 2 characters"}), 400

    if User.query.filter_by(email=email).first():
        error = {"error": "User already exists"}
        return jsonify(error), 409

    if not validate_password(password):
        return {
            "error": (
                "Password must be at least 8 characters long "
                "and contain uppercase, lowercase, and numeric characters."
            )
        }, 400

    if password != repeat_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if Company.query.filter_by(name=name).first():
        return jsonify({"error": "Company with this name already exists"}), 409
    hashed_pass = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        user = User(email=email, password=hashed_pass, role=role)
        db.session.add(user)
        db.session.flush()

        company = Company(user_id=user.user_id, name=name)
        db.session.add(company)
        db.session.commit()
        clear_cache_pattern("admin_")
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

    return jsonify({"success": "User created successfully!"}), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()

    if user.role == UserRoleEnum.admin:
        return jsonify({"email": user.email, "role": user.role.value}), 200
    elif user.role == UserRoleEnum.student:
        student = Student.query.filter_by(user_id=user_id).first()
        return jsonify(
            {
                "email": user.email,
                "role": user.role.value,
                "name": student.name,
                "roll_no": student.roll_no,
                "department": student.department or None,
            }
        ), 200
    elif user.role == UserRoleEnum.company:
        company = Company.query.filter_by(user_id=user_id).first()
        return jsonify(
            {
                "email": user.email,
                "role": user.role.value,
                "name": company.name,
                "approval_status": company.approval_status.value,
            }
        ), 200


@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)

    if (
        not data
        or "current_password" not in data
        or "new_password" not in data
        or "repeat_password" not in data
    ):
        return jsonify({"error": "Missing data fields"}), 400

    current_password = data["current_password"]
    new_password = data["new_password"]
    repeat_password = data["repeat_password"]

    if not bcrypt.check_password_hash(user.password, current_password):
        return jsonify({"error": "Current password is incorrect"}), 401

    if not validate_password(new_password):
        return jsonify(
            {
                "error": (
                    "Password must be at least 8 characters long "
                    "and contain uppercase, lowercase, and numeric characters."
                )
            }
        ), 400

    if new_password != repeat_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update password", "details": str(e)}), 500


def validate_password(password):
    if not isinstance(password, str):
        return False
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
    )


def validate_email(email):
    return isinstance(email, str) and EMAIL_RE.match(email) is not None


def normalize_text(value):
    return value.strip() if isinstance(value, str) else ""
