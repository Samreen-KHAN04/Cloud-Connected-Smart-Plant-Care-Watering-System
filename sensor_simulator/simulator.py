"""Virtual plant sensor. Run alone:  python -m sensor_simulator.simulator --interval 5"""
import argparse, math, os, random, time
from datetime import datetime


class Plant:
    def __init__(self):
        self.moisture, self.temp, self.humidity, self.tick = 60.0, 27.0, 55.0, 0

    def step(self, watered=False):
        self.tick += 1
        self.moisture = min(90, self.moisture + 30) if watered else max(5, self.moisture - random.uniform(1, 2))
        hour = datetime.now().hour
        self.temp = 28 + 6 * math.sin(self.tick / 20) + random.uniform(-.3, .3)
        self.humidity = max(20, min(95, 60 - (self.temp - 28) * 2 + random.uniform(-1, 1)))
        light = 0 if hour < 6 or hour > 18 else round(300 + 600 * math.sin(math.pi * (hour - 6) / 12))
        return {"device_id": "plant-1", "moisture": round(self.moisture, 1), "temperature": round(self.temp, 1),
                "humidity": round(self.humidity, 1), "light": light}


def main():
    import requests
    p = argparse.ArgumentParser()
    p.add_argument("--interval", type=float, default=5)
    p.add_argument("--url", default="http://127.0.0.1:8000")
    a = p.parse_args()
    key = os.getenv("API_KEY", "change-me")
    plant, watered = Plant(), False
    while True:
        data = plant.step(watered)
        try:
            r = requests.post(a.url + "/api/sensors/data", json=data, headers={"X-API-Key": key}, timeout=5)
            r.raise_for_status()
            watered = r.json().get("water", False)
            print("sent", data, "-> watered" if watered else "")
        except Exception as e:
            print("Server not reachable, will retry:", e)
            watered = False
        time.sleep(a.interval)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
