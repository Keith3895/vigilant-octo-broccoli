import pytest

def test_ping(app,test_client):
    rv = test_client.get('/hello')
    assert b'Hello, World!' in rv.data