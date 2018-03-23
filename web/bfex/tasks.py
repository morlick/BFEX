import os

from elasticsearch_dsl import connections
from bfex.celery import celery_instance as celery
from celery.signals import worker_process_init


@worker_process_init.connect
def init_worker(**kwargs):
    """Initializes elasticsearch connection"""
    elastic_host = os.getenv("ELASTIC_HOST", "localhost")
    connections.create_connection(hosts=[elastic_host])


@celery.task(name="Run Workflow", serializer="pickle")
def run_workflow(workflow):
    """Triggers workflow tasks"""
    workflow.run()
    print("COMPLETED RUNNING WORKFLOW!!!")