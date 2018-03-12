from bfex.celery import celery_instance as celery


@celery.task(name="Add_2_to_x")
def add_2(x):
    return x + 2
