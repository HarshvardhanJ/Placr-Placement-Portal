from flask import Blueprint, jsonify
from app.models.user import RoleEnum
from app.utils.decorators import role_required


admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@role_required(RoleEnum.admin)
def admin_dashboard():
    return jsonify({"message": "welcome admin"}), 200
