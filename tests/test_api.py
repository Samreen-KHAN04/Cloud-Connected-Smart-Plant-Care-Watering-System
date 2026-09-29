import os
os.environ.update(DATABASE_URL="sqlite:///test_plantcare.db", AUTO_SIMULATOR="false", API_KEY="k")
from fastapi.testclient import TestClient
from backend.app import app

H = {"X-API-Key": "k"}
good = dict(device_id="plant-1", moisture=60, temperature=25, humidity=50, light=500)


def test_flow():
    with TestClient(app) as c:
        assert c.post("/api/sensors/data", json=good).status_code == 401
        assert c.post("/api/sensors/data", json={**good, "moisture": 150}, headers=H).status_code == 422
        assert c.post("/api/sensors/data", json=good, headers=H).json()["water"] is False
        assert c.get("/api/devices/plant-1/summary").json()["status"] == "happy"
        r = c.post("/api/sensors/data", json={**good, "moisture": 10}, headers=H)
        assert r.json()["water"] is True
        assert any(a["kind"] == "low_moisture" for a in c.get("/api/alerts").json())
        assert len(c.get("/api/devices/plant-1/watering-history").json()) == 1
        c.post("/api/devices/plant-1/water")
        assert c.post("/api/sensors/data", json=good, headers=H).json()["water"] is True
        aid = c.get("/api/alerts").json()[0]["id"]
        assert c.put(f"/api/alerts/{aid}/acknowledge").json()["acknowledged"] is True
    from backend.app import engine
    engine.dispose()
    os.remove("test_plantcare.db")
