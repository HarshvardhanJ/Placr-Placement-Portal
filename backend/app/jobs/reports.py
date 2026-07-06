from datetime import datetime, timedelta

from flask import current_app, render_template_string
from app.jobs.celery_app import celery
from app.models.user import User, UserRoleEnum
from app.models.drive import Drive, DriveStatusEnum
from app.models.application import Application, ApplicationStatusEnum
from app.models.placement import Placement
from app.utils.email import send_report_mail


def get_previous_month_window(reference=None):
    reference = reference or datetime.utcnow()
    first_day_current_month = reference.replace(day=1, hour=0, minute=0, second=0)
    last_day_prev_month = first_day_current_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(
        day=1, hour=0, minute=0, second=0
    )

    return first_day_prev_month, first_day_current_month


@celery.task(namy="jobs.send_monthly_placement_report")
def send_monthly_placement_report():
    start_date, end_date = get_previous_month_window()

    admin = User.query.filter_by(role=UserRoleEnum.admin).first()
    if not admin:
        current_app.logger.exception("Monthly report: no admin found")
        return {"sent": False, "reason": "no admin user"}

    placement_report = {}
    placement_report["drives_conducted"] = Drive.query.filter(
        Drive.created_at >= start_date,
        Drive.created_at < end_date,
        Drive.approval_status == DriveStatusEnum.approved,
    ).count()

    placement_report["total_applications"] = Application.query.filter(
        Application.created_at >= start_date, Application.created_at < end_date
    ).count()

    placement_report["total_selected"] = Application.query.filter(
        Application.created_at >= start_date,
        Application.created_at < end_date,
        Application.status == ApplicationStatusEnum.selected,
    ).count()

    placement_report["total_placements"] = Placement.query.filter(
        Placement.created_at >= start_date, Placement.created_at < end_date
    ).count()

    try:
        send_report_mail(start_date, end_date, placement_report)
        current_app.logger.info("Monthly placement report sent")
        return {
            "sent": True,
            "drives_conducted": placement_report["drives_conducted"],
            "total_applications": placement_report["total_applications"],
            "total_selected": placement_report["total_selected"],
            "total_placements": placement_report["total_placements"],
        }
    except Exception:
        current_app.logger.exception("Failed sending report")
        return {"error": "could not send placement report"}
