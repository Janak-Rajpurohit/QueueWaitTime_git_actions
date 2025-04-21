from fastapi.testclient import TestClient
from app.app_main import app

client = TestClient(app)

def test_predict_success():
    payload = {
        "estimated_wait_time": 10,
        "join_method": "QR Join",
        "special_note": "None",
        "join_hour": 14,
        "join_dayofweek": 2,
        "time_taken_by_prev": 8.5,
        "index": 3
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_wait_time" in data
    assert "unit" in data
    assert data["unit"] == "minutes"
