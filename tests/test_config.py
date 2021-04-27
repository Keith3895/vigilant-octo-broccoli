import pytest

def test_testing_config(app,test_client):
    assert app.config['FLASK_ENV'] == 'TESTING'
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////tmp/test.db'