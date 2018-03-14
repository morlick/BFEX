import pytest
import os

class TestPersistTasks(object):

    @pytest.mark.skip(os.getenv("PYTEST_ENV", "dev") == "build")
    def test_persist_faculty():
        print("THE SKIPPED TEST IS RUNNING BUT IT SHOULDNT BE")
