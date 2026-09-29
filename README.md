# 🌱 Smart Plant Care

A website that shows how your plant is doing, waters it automatically when the soil is dry, and warns you about problems.
Pages: **Home**, **Live Data**, **Watering**, **Alerts**, **Help**.

## Run on Windows (VS Code)

1. Install Python 3.10+ from python.org (tick "Add Python to PATH").
2. In VS Code: File > Open Folder > choose this `PlantCare` folder. Open a terminal (Terminal > New Terminal, PowerShell).
3. Run these one at a time:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

4. Open http://127.0.0.1:8000 in your browser. A built-in virtual sensor starts automatically, so data appears within seconds.
5. Stop with Ctrl+C.

## Optional
- Separate sensor (set `AUTO_SIMULATOR=false` in `.env`, run the server, then in a 2nd terminal):
  `python -m sensor_simulator.simulator --interval 5`
- Run tests: `pytest`
- Technical API docs: http://127.0.0.1:8000/docs
- Change the sensor password in `.env` (`API_KEY`).

## Folders
- `frontend/` the five web pages
- `backend/app.py` server, database (SQLite file `plantcare.db`), watering rules, alerts
- `sensor_simulator/` virtual sensor
- `tests/` automatic checks
