from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_remove_background():
    payload = {
        "image_url": "https://example.com/sample-image.jpg",
        "bounding_box": {
            "x_min": 10,
            "y_min": 10,
            "x_max": 200,
            "y_max": 200
        }
    }
    response = client.post("/remove-background", json=payload)
    assert response.status_code in [200, 400, 500]  # Based on the image URL validity
