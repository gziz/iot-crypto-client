import logging
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()

from . import models, database, schemas
from .repository.data import read_send_data
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

        scheduler.add_job(read_send_data, 'cron', minute='*/15', id="000", replace_existing=True)

        scheduler.start()
        logger.info("Created Schedule Object")
    except:
        logger.error("Unable to Create Schedule Object")

@app.get("/")
def index():
    return "Hello!"
