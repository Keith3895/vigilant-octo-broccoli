import pytest
import os
import tempfile
from identity_server import create_app, models


@pytest.fixture
def app():
    flask_app = create_app('testing_config.py')
    with flask_app.app_context():
        models.db.init_app(flask_app)
        models.db.create_all()
        yield flask_app


@pytest.fixture
def test_client(app):

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!
    os.remove('/tmp/test.db')