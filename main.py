from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from apscheduler.schedulers.background import BackgroundScheduler
from starlette.websockets import WebSocket

from database import engine
from data import fetch_realtime_data
from routers import stops_router, map_router
from models import *

SQLModel.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(stops_router)
app.include_router(map_router)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_realtime_data, "interval", ["data/buffers"], minutes=1)
scheduler.start()


@app.on_event("shutdown")
def on_shutdown():
    scheduler.shutdown()
