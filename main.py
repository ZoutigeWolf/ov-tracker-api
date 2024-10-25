from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.websockets import WebSocket
from dotenv import load_dotenv

load_dotenv()

from database import engine
import database
from models import Agency
from routers import stops_router

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def a():
    await database.import_gtfs("/Users/zouti/Downloads/GTFS NL")

app.include_router(stops_router)
