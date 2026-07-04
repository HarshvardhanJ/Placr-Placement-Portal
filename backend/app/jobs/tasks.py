from app.jobs.celery_app import celery


@celery.task
def add(x, y):
    print(f"Adding {x} and {y}")
    return x + y
