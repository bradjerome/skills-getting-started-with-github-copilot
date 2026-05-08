import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

_initial_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))
    yield


@pytest.fixture
def client():
    return TestClient(app)
