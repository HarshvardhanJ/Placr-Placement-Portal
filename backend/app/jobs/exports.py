import csv
import os, time
from datetime import datetime
from flask import current_app

from app.jobs.celery_app import celery
from app.models.student import Student
from app.models.company import Company
from app.models.application import Application
from app.models.drive import Drive
from app.models.user import User
from app.utils.email import send_export_complete_mail


def _get_export_dir():
    export_dir = os.path.join(current_app.instance_path, "exports")
    os.makedirs(export_dir, exist_ok=True)
    return export_dir


def _student_row(application: Application):
    placement = application.placement
    drive = application.drive
    company = drive.company if drive else None

    return {
        "Application ID": application.application_id,
        "Job Title": drive.job_title if drive else "",
        "Company": company.name if company else "",
        "Applied On": application.application_date.isoformat()
        if application.application_date
        else "",
        "Status": application.status.value,
        "Interview Date": application.interview_date.isoformat()
        if application.interview_date
        else "",
        "Interview Type": application.interview_type.value
        if application.interview_type
        else "",
        "Remarks": application.remarks or "",
        "Offer Letter": placement.offer_letter_path if placement else "",
        "Joining Date": placement.joining_date.isoformat()
        if placement and placement.joining_date
        else "",
        "Salary (Offered)": placement.salary if placement else "",
    }


def _company_row(application):
    student = application.student
    drive = application.drive
    placement = application.placement

    return {
        "Application ID": application.application_id,
        "Student Name": student.name if student else "",
        "Roll No": student.roll_no if student else "",
        "Department": student.department if student else "",
        "CGPA": student.cgpa if student else "",
        "Job Title": drive.job_title if drive else "",
        "Applied On": application.application_date.isoformat()
        if application.application_date
        else "",
        "Status": application.status.value,
        "Interview Date": application.interview_date.isoformat()
        if application.interview_date
        else "",
        "Interview Type": application.interview_type.value
        if application.interview_type
        else "",
        "Selected": "Yes" if placement else "No",
        "Joining Date": placement.joining_date.isoformat()
        if placement and placement.joining_date
        else "",
        "Salary Offered": placement.salary if placement else "",
    }


@celery.task(name="jobs.export_student_history")
def export_student_history(user_id, email=None):
    try:
        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {
                "success": False,
                "reason": "Student profile not found",
            }
        applications = (
            Application.query.filter_by(student_id=student.student_id)
            .order_by(Application.created_at.desc())
            .all()
        )
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_roll = (student.roll_no or "na").replace("/", "_")

        filename = f"student_{safe_roll}_applications_{timestamp}.csv"

        filepath = os.path.join(_get_export_dir(), filename)

        fieldnames = [
            "Application ID",
            "Job Title",
            "Company",
            "Applied On",
            "Status",
            "Interview Date",
            "Interview Type",
            "Remarks",
            "Offer Letter",
            "Joining Date",
            "Salary (Offered)",
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for application in applications:
                writer.writerow(_student_row(application))

        recipient = email or student.user.email

        try:
            send_export_complete_mail(
                to=recipient,
                role="Student",
                filename=filename,
                count=len(applications),
            )
        except Exception:
            current_app.logger.exception("Failed sending student export email")

        current_app.logger.info(
            "Student export completed (%d records)",
            len(applications),
        )

        return {
            "success": True,
            "records": len(applications),
            "filename": filename,
            "download_url": f"/api/student/exports/download/{filename}",
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        current_app.logger.exception("Student export failed")

        return {
            "success": False,
            "error": str(e),
        }


@celery.task(name="jobs.export_company_history")
def export_company_history(user_id, email=None):
    try:
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {
                "success": False,
                "reason": "Company profile not found",
            }

        applications = (
            Application.query.join(Application.drive)
            .filter(Drive.company_id == company.company_id)
            .order_by(Application.created_at.desc())
            .all()
        )
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        safe_name = "".join(
            c if c.isalnum() or c in "-_" else "_" for c in (company.name or "na")
        )

        filename = f"company_{safe_name}_applications_{timestamp}.csv"

        filepath = os.path.join(_get_export_dir(), filename)

        fieldnames = [
            "Application ID",
            "Student Name",
            "Roll No",
            "Department",
            "CGPA",
            "Job Title",
            "Applied On",
            "Status",
            "Interview Date",
            "Interview Type",
            "Selected",
            "Joining Date",
            "Salary Offered",
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for application in applications:
                writer.writerow(_company_row(application))

        recipient = email or company.user.email

        try:
            send_export_complete_mail(
                to=recipient,
                role="Company",
                filename=filename,
                count=len(applications),
            )
        except Exception:
            current_app.logger.exception("Failed sending company export email")

        current_app.logger.info(
            "Company export completed (%d records)",
            len(applications),
        )

        return {
            "success": True,
            "records": len(applications),
            "filename": filename,
            "download_url": f"/api/company/exports/download/{filename}",
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        current_app.logger.exception("Company export failed")

        return {
            "success": False,
            "error": str(e),
        }


@celery.task(name="jobs.cleanup_exports")
def cleanup_exports(max_age_hours=24):
    now = time.time()
    removed = 0
    if not os.path.exists(_get_export_dir()):
        current_app.logger.info({"Removed old exports": removed})
        return
    for fname in os.listdir(_get_export_dir()):
        fpath = os.path.join(_get_export_dir(), fname)
        if (
            os.path.isfile(fpath)
            and (now - os.path.getmtime(fpath)) > max_age_hours * 3600
        ):
            try:
                os.remove(fpath)
            except OSError:
                pass
        current_app.logger.info({"Removed old exports": removed})
        return
