from datetime import date, datetime
import socket
from app.extensions import mail
from flask_mail import Message
from flask import render_template_string
from app.models.application import Application
from app.models.drive import Drive
from app.models.student import Student
from datetime import timedelta

socket.setdefaulttimeout(10)


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


def send_report_mail(
    start_date: datetime,
    end_date: datetime,
    placement_report: dict,
):
    msg = Message(
        subject=f"Monthly Placement Report - {start_date.strftime('%B %Y')}",
        recipients=["24f2001360@ds.study.iitm.ac.in"],
    )

    msg.body = "Hello Admin"

    msg.html = render_template_string(
        """
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Monthly Placement Report</h2>
                <p><strong>Period:</strong> {{ start_date }} to {{ end_date }}</p>
                <table border="1" cellpadding="8" cellspacing="0">
                    <tr><td>Drives Conducted</td><td>{{ drives_conducted }}</td></tr>
                    <tr><td>Total Applications</td><td>{{ total_applications }}</td></tr>
                    <tr><td>Students Selected</td><td>{{ total_selected }}</td></tr>
                    <tr><td>Total Placements</td><td>{{ total_placements }}</td></tr>
                </table>
            </body>
            </html>
            """,
        start_date=start_date.strftime("%d-%m-%Y"),
        end_date=(end_date - timedelta(seconds=1)).strftime("%d-%m-%Y"),
        drives_conducted=placement_report["drives_conducted"],
        total_applications=placement_report["total_applications"],
        total_selected=placement_report["total_selected"],
        total_placements=placement_report["total_placements"],
    )
    mail.send(msg)


def send_export_complete_mail(
    role, filename, count, to="24f2001360@ds.study.iitm.ac.in"
):
    msg = Message(
        subject=f"[Placement Portal] Your {role} export is ready", recipients=[to]
    )

    msg.body = f"""
        Hello,

        Your application history export has been completed successfully.

        • Role        : {role}
        • Records     : {count}
        • File name   : {filename}
        • Generated at: {datetime.utcnow().isoformat()} UTC

        Please log in to the Placement Portal and use the
        "Download Export" option to fetch your CSV file.

        Regards,
        Placr
        """

    mail.send(msg)
