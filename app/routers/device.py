import yaml
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..repository import device
from ..database import get_db
from .. import schemas, database, models

router = APIRouter(prefix = "/device", tags = ["Sensor Data"])

@router.get("/{key}")
async def get_value(key: str, db: Session = Depends(get_db)):
    return device.get_value(key, db)


@router.get("/")
async def get_all(db: Session = Depends(get_db)):
    return device.get_all(db)


@router.post("/")
async def insert_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    return device.insert_value(req, db)

@router.put("/")
async def update_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    return device.update_value(req, db)


@router.get('/init-db')
def init_db(db: Session = Depends(get_db)):
    if not db.query(models.KeyValue).first():
        with open('app/defaults.yaml', 'r') as f:
            defaults = yaml.safe_load(f)

        defaults = [models.KeyValue(key=key, value=val) for key, val in defaults.items()]

        db.add_all(defaults)
        db.commit()
        return {'message': 'Database initialized with default values'}
    else:
        return {'message': 'Database already contains data'}
