import os
from flask import Flask
from bfex.blueprints.data_ingestion import data_ingestion_bp as data_ingestion
from bfex.models import initialize_models


def create_app():
    from elasticsearch_dsl.connections import connections
    connections.create_connection(hosts=["localhost"])

    app = Flask("bfex")

    initialize_models()

    app.register_blueprint(data_ingestion)

    return app


