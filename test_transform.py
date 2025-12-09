import pytest
from main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_basic_english(client):
    resp = client.post('/transform', json={"text": "Hello world"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"tokens": ["hello", "world"], "count": 2, "has_numbers": False}


def test_spanish_preserve_accents(client):
    resp = client.post('/transform', json={"text": "¡Hola mundo cruel!", "language": "spanish"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["tokens"] == ["¡hola", "mundo", "cruel!"]
    assert data["count"] == 3
    assert data["has_numbers"] is False


def test_has_numbers_true(client):
    resp = client.post('/transform', json={"text": "Order 123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["has_numbers"] is True


def test_missing_text(client):
    resp = client.post('/transform', json={})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "missing required field 'text'"}


def test_text_not_string(client):
    resp = client.post('/transform', json={"text": 123})
    assert resp.status_code == 400


def test_invalid_language(client):
    resp = client.post('/transform', json={"text": "hi", "language": "german"})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "unsupported language"}


def test_non_json_body(client):
    resp = client.post('/transform', data='not json', content_type='text/plain')
    assert resp.status_code == 400
