from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User
from functools import wraps
from app.models.company import Company, CompanyStatusEnum


def role_required(role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user.role != role:
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)

        return wrapper

    return decorator


def approved_company_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"error": "Company not found"}), 404

        if company.approval_status != CompanyStatusEnum.approved:
            return jsonify({"error": "Company approval pending"}), 403

        return f(*args, **kwargs)

    return wrapper
