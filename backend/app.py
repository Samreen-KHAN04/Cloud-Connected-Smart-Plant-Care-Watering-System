"""Smart Plant Care API + website. Everything a browser needs is served from here."""
import os, threading, time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, desc, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()
API_KEY = os.getenv("API_KEY", "change-me")
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///plantcare.db"), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine, expire_on_commit=False)
now = lambda: datetime.utcnow()
COOLDOWN_SEC, OFFLINE_SEC, HOT_C = 60, 30, 35


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = "devices"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    threshold: Mapped[float] = mapped_column(Float, default=35)
    pending_water: Mapped[bool] = mapped_column(Boolean, default=False)


class Reading(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String, index=True)
    ts: Mapped[datetime] = mapped_column(DateTime, default=now)
    moisture: Mapped[float] = mapped_column(Float)
    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    light: Mapped[float] = mapped_column(Float)


class Watering(Base):
    __tablename__ = "watering"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String, index=True)
    ts: Mapped[datetime] = mapped_column(DateTime, default=now)
    kind: Mapped[str] = mapped_column(String)  # automatic | manual
    moisture_before: Mapped[float] = mapped_column(Float)


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String)
    ts: Mapped[datetime] = mapped_column(DateTime, default=now)
    kind: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)


class ReadingIn(BaseModel):
    device_id: str = "plant-1"
    moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-20, le=70)
    humidity: float = Field(ge=0, le=100)
    light: float = Field(ge=0, le=100000)


class ThresholdIn(BaseModel):
    threshold: float = Field(ge=5, le=80)


def row(o):
    out = {}
    for c in o.__table__.columns:
        v = getattr(o, c.name)
        out[c.name] = v.isoformat() + "Z" if isinstance(v, datetime) else v
    return out


def get_db():
    with SessionLocal() as db:
        yield db


def device_or_404(db, did):
    d = db.get(Device, did)
    if not d:
        raise HTTPException(404, "Device not found")
    return d


def last_reading(db, did):
    return db.scalars(select(Reading).where(Reading.device_id == did).order_by(desc(Reading.ts)).limit(1)).first()


def raise_alert(db, did, kind, msg):
    open_ = db.scalars(select(Alert).where(Alert.device_id == did, Alert.kind == kind, Alert.acknowledged == False)).first()  # noqa
    if not open_:
        db.add(Alert(device_id=did, kind=kind, message=msg))


def ingest(db: Session, r: ReadingIn) -> dict:
    d = db.get(Device, r.device_id)
    if not d:
        d = Device(id=r.device_id, name=r.device_id)
        db.add(d)
    db.add(Reading(**r.model_dump()))
    water = False
    if d.pending_water:
        d.pending_water, water = False, True
        db.add(Watering(device_id=d.id, kind="manual", moisture_before=r.moisture))
    elif r.moisture < d.threshold:
        last = db.scalars(select(Watering).where(Watering.device_id == d.id).order_by(desc(Watering.ts)).limit(1)).first()
        if not last or now() - last.ts > timedelta(seconds=COOLDOWN_SEC):
            water = True
            db.add(Watering(device_id=d.id, kind="automatic", moisture_before=r.moisture))
        raise_alert(db, d.id, "low_moisture", f"The soil is dry ({r.moisture:.0f}%). The plant was watered automatically.")
    if r.temperature > HOT_C:
        raise_alert(db, d.id, "high_temperature", f"It is very hot ({r.temperature:.0f} °C). Consider moving the plant to shade.")
    db.commit()
    return {"stored": True, "water": water}


def simulator_loop():
    from sensor_simulator.simulator import Plant
    plant, water = Plant(), False
    while True:
        with SessionLocal() as db:
            water = ingest(db, ReadingIn(**plant.step(water)))["water"]
        time.sleep(3)


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if not db.get(Device, "plant-1"):
            db.add(Device(id="plant-1", name="My Plant"))
            db.commit()
    if os.getenv("AUTO_SIMULATOR", "true").lower() == "true":
        threading.Thread(target=simulator_loop, daemon=True).start()
    yield


app = FastAPI(title="Smart Plant Care", lifespan=lifespan)


@app.get("/api/devices")
def devices(db: Session = Depends(get_db)):
    out = []
    for d in db.scalars(select(Device)):
        lr = last_reading(db, d.id)
        out.append({**row(d), "online": bool(lr and now() - lr.ts < timedelta(seconds=OFFLINE_SEC))})
    return out


@app.post("/api/sensors/data")
def post_data(r: ReadingIn, x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if x_api_key != API_KEY:
        raise HTTPException(401, "Invalid API key")
    return ingest(db, r)


@app.get("/api/devices/{did}/latest")
def latest(did: str, db: Session = Depends(get_db)):
    device_or_404(db, did)
    lr = last_reading(db, did)
    return row(lr) if lr else None


@app.get("/api/devices/{did}/history")
def history(did: str, limit: int = 60, db: Session = Depends(get_db)):
    device_or_404(db, did)
    rows = db.scalars(select(Reading).where(Reading.device_id == did).order_by(desc(Reading.ts)).limit(limit)).all()
    return [row(x) for x in reversed(rows)]


@app.get("/api/devices/{did}/summary")
def summary(did: str, db: Session = Depends(get_db)):
    """Plain-English status for non-technical users."""
    d, lr = device_or_404(db, did), last_reading(db, did)
    if not lr:
        return {"status": "waiting", "headline": "Waiting for the first reading", "advice": "Wait a few seconds or start the sensor simulator."}
    if now() - lr.ts > timedelta(seconds=OFFLINE_SEC):
        return {"status": "offline", "headline": "The sensor is not responding", "advice": "Check that the sensor or simulator is running."}
    if lr.temperature > HOT_C:
        return {"status": "hot", "headline": "Your plant is too hot", "advice": "Move it out of direct sun."}
    if lr.moisture < d.threshold:
        return {"status": "thirsty", "headline": "Your plant is thirsty", "advice": "Watering is happening automatically."}
    return {"status": "happy", "headline": "Your plant is happy", "advice": "Soil moisture, warmth and humidity look good."}


@app.put("/api/devices/{did}/threshold")
def set_threshold(did: str, t: ThresholdIn, db: Session = Depends(get_db)):
    d = device_or_404(db, did)
    d.threshold = t.threshold
    db.commit()
    return row(d)


@app.post("/api/devices/{did}/water")
def water_now(did: str, db: Session = Depends(get_db)):
    d = device_or_404(db, did)
    d.pending_water = True
    db.commit()
    return {"queued": True, "message": "Watering will happen at the next sensor reading."}


@app.get("/api/devices/{did}/watering-history")
def watering_history(did: str, db: Session = Depends(get_db)):
    device_or_404(db, did)
    return [row(x) for x in db.scalars(select(Watering).where(Watering.device_id == did).order_by(desc(Watering.ts)).limit(50))]


@app.get("/api/alerts")
def alerts(db: Session = Depends(get_db)):
    return [row(x) for x in db.scalars(select(Alert).order_by(desc(Alert.ts)).limit(100))]


@app.put("/api/alerts/{aid}/acknowledge")
def ack(aid: int, db: Session = Depends(get_db)):
    a = db.get(Alert, aid)
    if not a:
        raise HTTPException(404, "Alert not found")
    a.acknowledged = True
    db.commit()
    return row(a)


app.mount("/", StaticFiles(directory=Path(__file__).parent.parent / "frontend", html=True), name="site")
