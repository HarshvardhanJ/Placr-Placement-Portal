from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY"])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = FlaskTask

    celery.autodiscover_tasks(["app.jobs"])

    celery.conf.beat_schedule = {}

    return celery


def create_celery():
    from app import create_app

    app = create_app()
    return make_celery(app)


celery = create_celery()
