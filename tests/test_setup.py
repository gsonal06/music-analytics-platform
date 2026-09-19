from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_invalid_stream_count():
    response = client.post(
        "/ingest",
        json={
            "stream_id": 9999,
            "song_id": 1,
            "country_id": 1,
            "stream_date": "2026-09-01",
            "stream_count": -100
        }
    )

    assert response.status_code == 400


def test_top_songs():
    response = client.get("/analytics/top-songs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)