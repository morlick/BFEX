import pytest
import os

import elasticsearch_dsl as es
from test.conftest import is_dev_env


class TestPersistTasks(object):
    """Example of how to write a test that will not run on your dev machine."""

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_persist_faculty(self):
        assert es.connections.get_connection()
