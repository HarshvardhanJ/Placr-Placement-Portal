from datetime import datetime, timedelta
from app.utils.email import send_interview_reminder
from app.jobs.celery_app import celery
from app.models.application import Application, ApplicationStatusEnum


@celery.task(name="jobs.interview-reminder")
def interview_reminder():
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)

    print(now)
    print(tomorrow)

    interviews = Application.query.filter(
        Application.status == ApplicationStatusEnum.shortlisted,
        Application.interview_date >= now,
        Application.interview_date <= tomorrow,
    ).all()

    print(f"Found {len(interviews)} interviews")

    for application in interviews:
        send_interview_reminder(application.student, application.drive, application)
        print(application.student.user.email)
