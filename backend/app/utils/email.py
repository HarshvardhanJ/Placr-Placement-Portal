from app.extensions import mail
from flask_mail import Message

from app.models.application import Application
from app.models.drive import Drive
from app.models.student import Student


def send_interview_reminder(student: Student, drive: Drive, application: Application):
    msg = Message(
        subject=f"Interview Reminder - {drive.company.name}",
        # recipients=[student.user.email],
        recipients=[
            "24f2001360@ds.study.iitm.ac.in"
        ],  # i can only send email to myself unless i use a custom domain
    )

    msg.body = f"""
    Hello {student.name},

    This is a reminder that you have an interview.

    Company: {drive.company.name}
    Role: {drive.job_title}
    Date: {application.interview_date}
    Mode: {application.interview_type.value}

    Best of Luck!
    - Placr
    """

    mail.send(msg)
