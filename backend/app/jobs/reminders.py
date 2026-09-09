from datetime import datetime, timedelta
from app.utils.email import send_interview_reminder
from app.jobs.celery_app import celery
from app.models.application import Application, ApplicationStatusEnum
from flask import current_app


@celery.task(name="jobs.interview-reminder")
def interview_reminder():
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)

    interviews = Application.query.filter(
        Application.status == ApplicationStatusEnum.shortlisted,
        Application.interview_date >= now,
        Application.interview_date <= tomorrow,
    ).all()

    sent = 0
    failed = 0
    for application in interviews:
        try:
            send_interview_reminder(application.student, application.drive, application)
            sent += 1
        except Exception:
            current_app.logger.exception(
                f"Failed sending reminder for application {application.application_id}"
            )
            failed += 1

    current_app.logger.info(
        "Batch interview reminders complete. Sent: %d, Failed: %d", sent, failed
    )

    return {
        "processed": len(interviews),
        "sent": sent,
        "failed": failed,
    }
