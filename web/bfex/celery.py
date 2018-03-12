import os

from celery import Celery
# from flask import current_app

def make_celery():
    # Configure Celery
    celery_broker = os.getenv("CELERY_BROKER", "redis://localhost:6379")
    celery_backend = os.getenv("CELERY_BACKEND", "redis://localhost:6379")

    celery = Celery("bfex_celery", broker=celery_broker, backend=celery_backend, imports=('bfex.tasks',))
    # celery.conf.update(app.config)
    # TaskBase = celery.Task
    #
    # class ContextTask(TaskBase):
    #     abstract = True
    #
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return TaskBase.__call__(self, *args, **kwargs)
    #
    # celery.Task = ContextTask
    return celery


celery_instance = make_celery()
