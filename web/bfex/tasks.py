import os

from elasticsearch_dsl import connections
from bfex.celery import celery_instance as celery
from celery.signals import worker_process_init


@worker_process_init.connect
def init_worker(**kwargs):
    elastic_host = os.getenv("ELASTIC_HOST", "localhost")
    connections.create_connection(hosts=[elastic_host])

@celery.task(name="Add_2_to_x")
def add_2(x):
    print("X IS {}".format(x))
    return x + 2


@celery.task(name="Run Workflow", serializer="pickle")
def run_workflow(workflow):
    workflow.run()
    print("COMPLETED RUNNING WORKFLOW!!!")