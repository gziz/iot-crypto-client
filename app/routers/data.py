import yaml
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..repository import data
from ..database import get_db
from .. import schemas, database, models


router = APIRouter(prefix = "/data", tags = ["Sensor Data"])

@router.post("/manual")
def send_data_manual(req: schemas.SensorData):
    return data.send_data_manual(req)

@router.post("/auto")
def send_data_auto():
    return data.read_send_data()