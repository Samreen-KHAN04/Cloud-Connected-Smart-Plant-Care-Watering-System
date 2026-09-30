# 🌱 Smart Plant Care

Smart Plant Care is a lightweight full-stack plant monitoring app that tracks soil moisture, temperature, humidity, and light levels for a plant. It displays live readings in a browser dashboard, automatically waters the plant when needed, and raises alerts when conditions become unhealthy.

## Features

- Live plant status dashboard
- Automatic watering based on soil moisture thresholds
- Manual watering queue for immediate watering requests
- Alert system for low moisture and overheating
- SQLite-backed history and recent readings
- Built-in virtual sensor simulator for demo/testing
- Simple REST API for sensor input and device management

## Technology Used

This project uses a lightweight full-stack web architecture:

- Python for the backend logic and API
- FastAPI for the web API and routing
- Uvicorn as the ASGI server
- SQLAlchemy for database models and queries
- SQLite for local data storage
- HTML, CSS, and JavaScript for the frontend interface
- pytest for automated testing
- python-dotenv for environment configuration
- requests and httpx for client-side HTTP interactions

## Pages

The app includes these pages:

- Home
- Live Data
- Watering
- Alerts
- Help

## Learnings

This project demonstrates key skills in building a practical web application:

- Full-stack development using a Python backend and browser frontend
- Creating REST APIs with FastAPI
- Managing persistent data with SQLite and SQLAlchemy
- Designing simple dashboards and user interfaces with HTML, CSS, and JavaScript
- Working with automated sensor data and real-time status updates
- Handling alerts, device state, and automation logic
- Writing and running tests to validate API behavior
- Structuring a small project with reusable modules and clean file organization

## Project Structure

```text
PlantCare/
├── backend/
│   └── app.py
├── frontend/
│   ├── alerts.html
│   ├── app.js
│   ├── dashboard.html
│   ├── help.html
│   ├── index.html
│   ├── style.css
│   └── watering.html
├── sensor_simulator/
│   ├── __init__.py
│   └── simulator.py
├── tests/
│   └── test_api.py
├── main.py
├── README.md
├── requirements.txt
├── .env (optional)
└── plantcare.db (generated at runtime)
```

## Requirements

- Python 3.10+
- A browser such as Chrome or Edge
- PowerShell or a terminal on Windows

## Quick Start on Windows

1. Install Python 3.10+ from python.org and make sure "Add Python to PATH" is enabled.
2. Open the project folder in VS Code.
3. Open a terminal in the project root.
4. Run the following commands:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

If PowerShell blocks script execution, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

5. Open http://127.0.0.1:8000 in your browser.
6. Press Ctrl+C in the terminal to stop the app.

The app starts a built-in virtual sensor automatically, so readings should appear within a few seconds.

## Environment Variables

You can optionally create a `.env` file in the project root to configure the app:

```env
API_KEY=your-secret-key
DATABASE_URL=sqlite:///plantcare.db
AUTO_SIMULATOR=true
```

Notes:

- `API_KEY` is used to validate sensor submissions.
- `DATABASE_URL` changes the database location.
- `AUTO_SIMULATOR=false` disables the built-in virtual sensor.

## Running the Sensor Simulator Separately

If you want to use a separate sensor process instead of the built-in simulator:

```powershell
$env:AUTO_SIMULATOR = "false"
python main.py
```

Then, in a second terminal:

```powershell
python -m sensor_simulator.simulator --interval 5
```

## API

The app exposes a FastAPI API and Swagger documentation is available at:

- http://127.0.0.1:8000/docs

Key endpoints include:

- `GET /api/devices` - list devices
- `GET /api/devices/{id}/latest` - latest reading for a device
- `GET /api/devices/{id}/history` - sensor history
- `GET /api/devices/{id}/summary` - plain-English plant status
- `PUT /api/devices/{id}/threshold` - update moisture threshold
- `POST /api/devices/{id}/water` - request manual watering
- `GET /api/alerts` - current alerts
- `PUT /api/alerts/{id}/acknowledge` - acknowledge an alert

## Testing

Run the test suite with:

```powershell
pytest
```

## Troubleshooting

- If the app does not start, confirm Python and dependencies are installed correctly.
- If the dashboard shows no data, check that the simulator is running.
- If the port 8000 is already in use, change the port in `main.py` or stop the other service.
- If API requests fail, ensure the `X-API-Key` header matches the value in your `.env` file.

## Notes

This project is designed as a simple demonstration of an IoT-style smart garden system and is ideal for learning web APIs, SQLite storage, and sensor-driven automation.
