from fastapi.testclient import TestClient
from main import app
import re

client = TestClient(app)


def test_get_time():
    response = client.get("/time")
    assert response.status_code == 200
    data = response.json()

    # Debe existir la clave "time"
    assert "time" in data

    # Validar formato YYYY-MM-DD HH:MM:SS
    patron = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.match(patron, data["time"])

    # Aceptar tanto scraping como fallback local
    assert data.get("source") in ["scraping", "local"]
