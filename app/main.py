import logging
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from . import models, database, schemas
from .database import get_db
from .routers import data, device

app = FastAPI()
models.Base.metadata.create_all(database.engine)

app.include_router(data.router)
app.include_router(device.router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def load_schedule_or_create_blank():

    try:
        scheduler = BackgroundScheduler()

        schema = schemas.SensorData()
        scheduler.add_job(data.add_data_manual, 'cron', minute='*/5', id="000", replace_existing=True, args=[schema])

        scheduler.start()
        logger.info("Created Schedule Object")
    except:
        logger.error("Unable to Create Schedule Object")

@app.get("/")
def index():
    return "Hello!"
