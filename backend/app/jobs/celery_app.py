from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(app.import_name, include=["app.jobs.reminders", "app.jobs.reports"])
    celery.conf.update(app.config["CELERY"])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = FlaskTask

    celery.conf.beat_schedule = {
        "interview-reminder": {
            "task": "jobs.interview-reminder",
            "schedule": crontab(hour=6, minute=0),
        },
        "send-monthly-placement-report": {
            "task": "jobs.send_monthly_placement_report",
            "schedule": crontab(day_of_month=1, hour=12),
        },
    }

    return celery


def create_celery():
    from app import create_app

    app = create_app()
    return make_celery(app)


celery = create_celery()
