# 🌱 Cloud-Connected-Smart-Plant-Care-Watering-System

Smart Plant Care is a full-stack web application designed to monitor plant health, automate watering, and alert users when conditions become unsafe for the plant. The project simulates an Internet of Things (IoT) plant monitoring system using live sensor data, historical tracking, and a browser-based dashboard.

It is built as a practical solution for smart gardening and plant maintenance, combining backend automation with an interactive front-end interface.

## Project Overview

In real-world gardening and smart agriculture scenarios, plant health depends heavily on factors such as soil moisture, temperature, humidity, and light exposure. This project addresses that problem by monitoring those conditions and taking action when needed.

The system:

- tracks live plant readings from a virtual sensor
- detects low soil moisture and triggers automatic watering
- alerts users when the plant is overheated
- stores plant history in a database for later analysis
- provides a simple dashboard for monitoring device status and alerts

## Why This Project is Valuable

This project demonstrates a realistic use case for:

- IoT-style monitoring systems
- automation in smart agriculture
- data-driven decision making
- full-stack application development
- API-driven system design

It is also a strong project for a portfolio because it combines technical implementation with a clear business and user value.

## Key Features

- Live plant dashboard with real-time status updates
- Automatic watering based on soil moisture threshold
- Manual watering trigger for user-initiated watering requests
- Alert generation for low moisture and high temperature
- Historical reading storage and retrieval
- Device status tracking and online/offline detection
- REST API for sensor data ingestion and device management
- Built-in virtual sensor simulation for testing and demos
- SQLite-backed persistence for lightweight local data storage

## Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Tools and Utilities
- pytest
- python-dotenv
- requests
- httpx

## System Architecture

The application follows a simple three-layer architecture:

1. Frontend layer
   - Browser-based UI served from static HTML, CSS, and JavaScript files
2. Backend layer
   - FastAPI app handles API endpoints, business logic, and device operations
3. Data layer
   - SQLite database stores readings, watering records, and alerts

The system also includes a sensor simulator that emulates live plant readings and sends those values to the backend automatically.

## Pages

The app includes the following pages:

- Home
- Live Data
- Watering
- Alerts
- Help

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

## Core Functionalities

### 1. Sensor Monitoring
The app monitors environmental conditions such as:

- soil moisture
- temperature
- humidity
- light intensity

### 2. Automatic Watering Logic
If the soil moisture drops below the configured threshold, the app automatically records a watering event and updates the plant state accordingly.

### 3. Alerting System
The system raises alerts for unhealthy conditions such as:

- low moisture
- excessive heat

### 4. Device Management
The backend supports device records and allows operations such as threshold updates and manual watering requests.

### 5. Historical Data Access
The application stores all readings and watering events to give users a track record of plant behavior over time.

## API Endpoints

The project exposes a FastAPI API with Swagger documentation available at:

- http://127.0.0.1:8000/docs

### Main endpoints

- `GET /api/devices` - list all registered devices
- `GET /api/devices/{id}/latest` - fetch the most recent sensor reading
- `GET /api/devices/{id}/history` - fetch past sensor readings
- `GET /api/devices/{id}/summary` - get a plain-English plant health summary
- `PUT /api/devices/{id}/threshold` - update the watering threshold
- `POST /api/devices/{id}/water` - queue manual watering
- `GET /api/alerts` - fetch active alerts
- `PUT /api/alerts/{id}/acknowledge` - mark an alert as acknowledged

## Skills and Learning Outcomes

This project demonstrates practical application of the following skills:

- Full-stack development with backend and frontend integration
- API design and implementation using FastAPI
- Database modeling and CRUD operations with SQLAlchemy
- Real-time data handling and automation logic
- IoT-inspired system design
- Front-end UI development with HTML, CSS, and JavaScript
- Data persistence and retrieval using SQLite
- Testing and validation with pytest
- Problem solving in real-world automation scenarios

## Installation and Setup

### Prerequisites

- Python 3.10+
- VS Code or any Python IDE
- Windows PowerShell or terminal
- Modern web browser

### Steps

1. Clone the repository.
2. Open the project folder in VS Code.
3. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Run the application:

```powershell
python main.py
```

6. Open the app in the browser:

```text
http://127.0.0.1:8000
```

7. To stop the app, press `Ctrl + C` in the terminal.

## Environment Variables

Create a `.env` file in the project root if needed:

```env
API_KEY=your-secret-key
DATABASE_URL=sqlite:///plantcare.db
AUTO_SIMULATOR=true
```

### Configuration notes

- `API_KEY` validates incoming sensor requests
- `DATABASE_URL` defines the database storage location
- `AUTO_SIMULATOR=false` disables the built-in simulator

## Running the Sensor Simulator Separately

If you want to run the simulator independently:

```powershell
$env:AUTO_SIMULATOR = "false"
python main.py
```

Then in a second terminal:

```powershell
python -m sensor_simulator.simulator --interval 5
```

## Testing

Run the test suite with:

```powershell
pytest
```

## Potential Future Enhancements

- real-time charts and analytics dashboard
- email or SMS notifications
- dark mode and improved UI/UX
- plant health prediction with ML
- user authentication and multi-device support
- deployment to cloud platforms

## Troubleshooting

- If the app does not start, verify Python and dependencies are installed correctly.
- If no readings appear, confirm the sensor simulator is running.
- If port 8000 is occupied, stop the conflicting process or change the port.
- If API requests fail, ensure the correct `API_KEY` is configured.

## Project Impact

This project reflects a practical approach to solving a real-world problem: helping users monitor plant health and reduce the risk of dehydration or heat stress. It is a strong example of how software can improve everyday life by combining automation, monitoring, and analytics.

## Conclusion

Smart Plant Care is a portfolio-ready project that demonstrates practical software engineering, backend logic, UI development, and automation. It is suitable for showcasing problem-solving ability, API design skills, and the ability to build a complete real-world application from concept to execution.

