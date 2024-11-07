import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from apscheduler.schedulers.background import BackgroundScheduler
from starlette.websockets import WebSocket
from contextlib import asynccontextmanager

from database import engine
from data import fetch_realtime_data
from routers import stops_router, map_router

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(fetch_realtime_data, "interval", ["data/buffers"], minutes=1)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(stops_router)
app.include_router(map_router)
