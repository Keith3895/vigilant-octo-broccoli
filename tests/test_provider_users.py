import pytest
import json


def test_register_without_full(test_client):
    """Ensure a new user can be added to the database."""
    response = test_client.post(
        '/oauth/register',
        data=json.dumps(dict(
            email='michael@something.com',
            password='massword',
            first_name='michael',
            last_name='something',
            # full_name='michael something'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert 'michael@something.com' in data['user']


def test_register(test_client):
    """Ensure a new user can be added to the database."""
    response = test_client.post(
        '/oauth/register',
        data=json.dumps(dict(
            email='michael@something.com',
            password='massword',
            first_name='michael',
            last_name='something',
            full_name='michael something'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert 'michael@something.com' in data['user']
